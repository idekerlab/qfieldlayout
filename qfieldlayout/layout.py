#
# The layout object defines the datastructures
# and parameters for the algorithm.
#
import numpy as np
from qfieldlayout import network
from math import sqrt
from qfieldlayout.fields import repulsion_field, attraction_field, add_field, subtract_field

import logging

logger = logging.getLogger(__name__)

# TODO
# add a mask parameter
# the nodes have integer tags specifying regions
# They are only allowed to be placed in those regions after the initial positions
# The regions are specified as vectors of coordinates.
# In the simple case, the regions would not overlap.
# But maybe there is a use case for overlapping regions.
# There will be two masks to begin with:
# a simple geometric case for testing
# a classic cell diagram:
# extracellular - set the whole g-field = 0
# cell membrane - a circle = 1
# cytoplasm - a smaller circle = 2
# nuclear membrane - a smaller circle = 3
# nucleus - a smaller circle = 4
class QFLayout:
    def __init__(self, input_network, sparsity=30, r_radius=10,
                 a_radius=10, r_scale=10, a_scale=5, center_attractor_scale=0.01,
                 initialize_coordinates="spiral", datatype=np.int16):
        self.integer_type = datatype
        self.network = input_network

        self.gfield, center = self._make_gfield(sparsity, center_attractor_scale)
        self.gfield_mask = np.zeros(self.gfield.shape, dtype=self.integer_type)

        if initialize_coordinates == "center":
            logger.debug("init at center")
            self.network.place_nodes_at_center(center)
        elif initialize_coordinates == "random":
            logger.debug("init random")
            self.network.place_nodes_randomly(self.gfield.shape[0])
        elif initialize_coordinates == "spiral":
            logger.debug("init spiral")
            self.network.place_nodes_in_a_spiral(center)

        self.rfield = repulsion_field(r_radius, r_scale, self.integer_type, center_spike=True)
        self.afield = attraction_field(a_radius, a_scale, self.integer_type)
        self.afield_med = attraction_field(a_radius, a_scale * 5, self.integer_type)
        self.afield_high = attraction_field(a_radius, a_scale * 10, self.integer_type)
        # make a scratchpad board where we add all the attraction fields
        # and the use it to update the gfield
        self.sfield = np.zeros(self.gfield.shape, self.integer_type)

        # initialize the repulsion field and the mask
        for node in self.network.get_sorted_nodes():
            add_field(self.rfield, self.gfield, node["x"], node["y"])
            self.gfield_mask[node["x"], node["y"]] = 1

    @classmethod
    def from_nicecx(cls, nicecx, **kwargs):
        return cls(network.QFNetwork.from_nicecx(nicecx), **kwargs)

    def _make_gfield(self, sparsity, center_attractor_scale):
        radius = round(sqrt(self.network.get_nodecount() * sparsity))
        dimension = (2 * radius) + 1
        board = np.zeros((dimension, dimension), dtype=self.integer_type)
        # nodes are pulled towards the center of the gfield
        # by giving the gfield an attraction field at its center
        # the radius of the field is the distance from the center to the corners
        center = int(board.shape[0] / 2)
        center_attractor_radius = int(sqrt(2 * center ** 2))
        add_field(attraction_field(center_attractor_radius, center_attractor_scale, self.integer_type),
                  board,
                  center, center)
        return board, center

    # update the position of one node
    def layout_one_node(self, node):
        # remove the node from the gfield by subtracting its rfield at its current location
        subtract_field(self.rfield, self.gfield, node['x'], node['y'])

        # clear the "scratchpad" sfield
        self.sfield[...] = 0
        # add the afields to the sfield
        degree = node["degree"]
        for adj_node_id in node['adj']:
            # add an afield to the sfield
            # lower degree nodes have higher afields
            adj_node = self.network.node_dict[adj_node_id]
            if degree == 1:
                add_field(self.afield_high, self.sfield, adj_node["x"], adj_node["y"])
            elif degree < 5:
                add_field(self.afield_med, self.sfield, adj_node["x"], adj_node["y"])
            else:
                add_field(self.afield, self.sfield, adj_node["x"], adj_node["y"])

        # add sfield to the gfield
        self.gfield += self.sfield

        # The destination is a location with the minimum value.
        # argmin returns the index of the first location containing
        # the minimum value in a flattened version of the array.
        # unravel_index turns the index back into the coordinates.
        destination = np.unravel_index(np.argmin(self.gfield, axis=None), self.sfield.shape)

        # the constraint that we do not place two nodes at the
        # same location is satisfied by (1) setting the center of
        # the rfield to a "spike", a value so high that it will
        # never be the minima and (2) initializing the nodes
        # with unique locations.

        node["x"] = destination[0]
        node["y"] = destination[1]
        # add the rfield at the destination
        add_field(self.rfield, self.gfield, destination[0], destination[1])
        # subtract the sfield to revert the gfield to contain only the superposition of node rfields.
        self.gfield -= self.sfield

    def do_layout(self, rounds=1, node_size=40):
        node_list = self.network.get_sorted_nodes()

        # perform the rounds of layout
        # start = timer()
        for n in range(0, rounds):
            logger.debug('round ' + str(n))
            for node in node_list:
                # degree = node.get("degree")
                # only layout the degree 1 nodes on the last
                # round
                # if degree > 1 or n >= (rounds-1):
                self.layout_one_node(node)

        # end = timer()
        # print("layout time = ", end - start)
        return self.network.get_cx_layout(node_size=node_size)
