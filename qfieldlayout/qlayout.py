# simplified layout for paper

import numpy as np
from qfieldlayout import network
from math import sqrt, log
from qfieldlayout.fields import repulsion_field, attraction_field, add_field, subtract_field

import logging

logger = logging.getLogger(__name__)

class QLayout:
    def __init__(self, input_network, sparsity=30, r_radius=10,
                 a_radius=10, r_scale=10, a_scale=10, a_base = 3, center_attractor_scale=0.01, datatype=np.int16, verbose=False):
        self.integer_type = datatype
        self.network = input_network
        self.gfield, center = self._make_gfield(sparsity, center_attractor_scale)
        self.sfield = np.zeros(self.gfield.shape, self.integer_type)
        self.rfield = repulsion_field(r_radius, r_scale, self.integer_type, center_spike=True)
        self.a_radius = a_radius
        self.a_scale = a_scale
        self.a_base = a_base
        self.afields = {1 : attraction_field(a_radius, a_scale, self.integer_type)}
        self.alpha = []

    @classmethod
    def from_nicecx(cls, nicecx, **kwargs):
        return cls(network.QFNetwork.from_nicecx(nicecx), **kwargs)

    # cache scaled afields as needed
    def _get_afield(self, degree):
        if self.afields.get(degree) is None:
            self.afields[degree] = attraction_field(self.a_radius, self.a_scale/degree + self.a_scale/self.a_base, self.integer_type)
        return self.afields[degree]

    def _make_gfield(self, sparsity, center_attractor_scale):
        radius = round(sqrt(self.network.get_nodecount() * sparsity))
        dimension = (2 * radius) + 1
        gf = np.zeros((dimension, dimension), dtype=self.integer_type)
        # nodes are pulled towards the center of the gfield
        # by giving the gfield an attraction field at its center
        # the radius of the field is the distance from the center to the corners
        center = int(gf.shape[0] / 2)
        center_attractor_radius = int(sqrt(2 * center ** 2))
        add_field(attraction_field(center_attractor_radius, center_attractor_scale, self.integer_type),
                  gf,
                  center, center)
        return gf, center

    def do_layout(self, rounds=1, threshold = None):
        node_list = self.network.get_sorted_nodes()
        # perform the rounds of layout
        # start = timer()
        for n in range(0, rounds):
            logger.debug('round ' + str(n))
            for node in node_list:
                self.update_node_position(node, n)
            if n > 0:
                alpha = self.compute_alpha(n)
                self.alpha.append(alpha)
                if threshold is not None and alpha < threshold:
                    return
                #print(self.alpha)


    def update_node_position(self, node, layout_round):
        # remove the node's repulsion field unless this is the first time it has been placed
        if node.get("x") is not None and node.get("y") is not None:
            subtract_field(self.rfield, self.gfield, node['x'], node['y'])

        # update the neighbor attraction field based on the nodes neighbors
        #
        # each node has a total amount of attraction that it distributes over all its neighbors.
        # a neighbor of a degree 1 node is given the full strength afield.
        # degree 1 nodes strongly 'want' to be next to their neighbor.
        # Vice versa, neighbors of a degree 20 node are each modeled as a 1/20 afield.
        # clear the "scratchpad" sfield
        self.sfield[...] = 0
        # get an afield based on the node's degree
        degree = node["degree"]
        af = self._get_afield(degree)

        # iterate over the adjacent nodes
        for adj_node_id in node['adj']:
            adj_node = self.network.node_dict[adj_node_id]
            # add the adjacent node's afield unless it does not yet have a position
            if adj_node.get("x") is not None and adj_node.get("y") is not None:
                add_field(af, self.sfield, adj_node["x"], adj_node["y"])

        # add neighbor attraction in the sfield to the gfield
        self.gfield += self.sfield

        # The destination is a location with the minimum value.
        # argmin returns the index of the first location containing
        # the minimum value in a flattened version of the array.
        # unravel_index turns the index back into the coordinates.
        destination = np.unravel_index(np.argmin(self.gfield, axis=None), self.sfield.shape)
        node["x"] = destination[0]
        node["y"] = destination[1]

        # add the rfield at the destination
        add_field(self.rfield, self.gfield, destination[0], destination[1])

        # update the node's energy
        node["energy"][layout_round] = self.gfield[destination[0], destination[1]]

        # subtract the sfield to revert the gfield to contain only the superposition of node rfields.
        self.gfield -= self.sfield

    def compute_alpha(self, layout_round):
        node_list = self.network.get_sorted_nodes()
        sum_node_change = 0
        for node in node_list:
            delta = abs(node["energy"][layout_round] - node["energy"][layout_round-1])
            node_change = delta/node["energy"][layout_round - 1]
            sum_node_change += node_change
        return sum_node_change/len(node_list)

    def get_cx_layout(self, scale):
        return self.network.get_cx_layout(node_size=scale)
