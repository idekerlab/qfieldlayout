# the layout described in the paper

import numpy as np
from qfieldlayout.qnetwork import adjacency_network_from_edge_array, get_sorted_node_list, get_cx_layout
from math import sqrt, log
from qfieldlayout.fields import repulsion_field, attraction_field, add_field, subtract_field
from qfieldlayout.qfigures import save_field_cross_section_plot, save_convergence_graph, save_field_heatmap

import logging

logger = logging.getLogger(__name__)


class QLayout:
    def __init__(self, edge_array, sparsity=30, r_radius=10,
                 a_radius=10, r_scale=10, a_scale=10, a_base=3, center_attractor_scale=0.01, datatype=np.int16,
                 make_figures=False):
        self.make_figures = make_figures
        self.edge_array = edge_array
        self.network = adjacency_network_from_edge_array(edge_array)
        self.integer_type = datatype
        self.a_radius = a_radius
        self.a_scale = a_scale
        self.a_base = a_base
        self.a_fields = {}
        self.network = adjacency_network_from_edge_array(edge_array)
        # cache a scaled a_field for each node degree found in the network
        for node in self.network.values():
            if self.a_fields.get(node["degree"]) is None:
                self.a_fields[node["degree"]] = attraction_field(self.a_radius,
                                                                 self.a_scale / node[
                                                                     "degree"] + self.a_scale / self.a_base,
                                                                 self.integer_type)
        self.convergence_history = []
        self.g_field, center = self._make_g_field(sparsity, center_attractor_scale)
        self.x_field = np.zeros(self.g_field.shape, self.integer_type)
        self.r_field = repulsion_field(r_radius, r_scale, self.integer_type, center_spike=True)

        if self.make_figures is True:
            save_field_cross_section_plot(self.r_field, filename="r_field_x_section")

    def _make_g_field(self, sparsity, center_attractor_scale):
        node_count = len(self.network.values())
        radius = round(sqrt(node_count * sparsity))
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

    def do_layout(self, layout_steps=1, convergence_threshold=None):
        node_list = get_sorted_node_list(self.network)
        # perform the rounds of layout
        # start = timer()
        for step in range(0, layout_steps):
            logger.debug('step ' + str(step))
            for node in node_list:
                self.update_node_position(node, step)
            if step > 0:
                convergence_score = self.compute_convergence_score(step)
                self.convergence_history.append(convergence_score)
                if convergence_threshold is not None and convergence_score < convergence_threshold:
                    break
        if self.make_figures is True:
            save_convergence_graph([self.convergence_history], filename="temp_convergence")
            save_field_heatmap(self.g_field, filename="final_g_field")

    def update_node_position(self, node, layout_step):
        # remove the node's repulsion field unless this is the first time it has been placed
        if node.get("x") is not None and node.get("y") is not None:
            subtract_field(self.r_field, self.g_field, node['x'], node['y'])

        # update the neighbor attraction field based on the nodes neighbors
        #
        # each node has a total amount of attraction that it distributes over all its neighbors.
        # a neighbor of a degree 1 node is given the full strength afield.
        # degree 1 nodes strongly 'want' to be next to their neighbor.
        # Vice versa, neighbors of a degree 20 node are each modeled as a 1/20 afield.

        # clear the "scratchpad" x_field - an optimization to reduce the number of matrix additions
        self.x_field[...] = 0

        # get an afield based on the node's degree
        degree = node["degree"]
        af = self.a_fields[degree]

        # iterate over the adjacent nodes
        for adj_node_id in node['adj']:
            adj_node = self.network[adj_node_id]
            # add the adjacent node's afield unless it does not yet have a position
            if adj_node.get("x") is not None and adj_node.get("y") is not None:
                add_field(af, self.x_field, adj_node["x"], adj_node["y"])

        # add neighbor attraction in the sfield to the gfield
        self.g_field += self.x_field

        # The destination is a location with the minimum value.
        # argmin returns the index of the first location containing
        # the minimum value in a flattened version of the array.
        # unravel_index turns the index back into the coordinates.
        destination = np.unravel_index(np.argmin(self.g_field, axis=None), self.x_field.shape)
        node["x"] = destination[0]
        node["y"] = destination[1]

        # add the rfield at the destination
        add_field(self.r_field, self.g_field, destination[0], destination[1])

        # update the node's energy
        node["energy"][layout_step] = self.g_field[destination[0], destination[1]]

        # subtract the sfield to revert the gfield to contain only the superposition of node rfields.
        self.g_field -= self.x_field

    def compute_convergence_score(self, layout_step):
        node_list = get_sorted_node_list(self.network)
        sum_node_change = 0
        for node in node_list:
            delta = abs(node["energy"][layout_step] - node["energy"][layout_step - 1])
            node_change = delta / node["energy"][layout_step - 1]
            sum_node_change += node_change
        return sum_node_change / len(node_list)

    def get_cx_layout(self, scale):
        return get_cx_layout(self.network, node_size=scale)
