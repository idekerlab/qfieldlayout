#
# A network data structure for layout and clustering
# The set of nodes is indexed by id
# Each node is a dict that has (at least) these attributes:
# adjacent nodes
# node degree
# name
# the node dict is sorted by degree
# the edges are a pandas dataframe
from itertools import count
import numpy as np
from operator import itemgetter
from random import randint
import logging

logger = logging.getLogger(__name__)


class QFNetwork:

    def __init__(self, edge_array, name="unnamed network") -> None:
        self.node_dict = {}
        for edge in edge_array:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(str(edge[0]) + ' ' + str(edge[1]))
            if edge[0] not in self.node_dict:
                self.node_dict[edge[0]] = {"adj": set(), "energy": {}}
            self.node_dict[edge[0]]["adj"].add(edge[1])
            self.node_dict[edge[0]]["degree"] = len(self.node_dict[edge[0]]["adj"])
            if edge[1] not in self.node_dict:
                self.node_dict[edge[1]] = {"adj": set(), "energy": {}}
            self.node_dict[edge[1]]["adj"].add(edge[0])
            self.node_dict[edge[1]]["degree"] = len(self.node_dict[edge[1]]["adj"])

    @classmethod
    def from_nicecx(cls, nicecx):
        edge_array = np.zeros((len(nicecx.get_edges()), 2), dtype=int)
        logger.debug("edge array: " + str(edge_array.shape))
        i = 0
        for edge_id, edge in nicecx.get_edges():
            edge_array[i, 0] = edge["s"]
            edge_array[i, 1] = edge["t"]
            i += 1
        return cls(edge_array, name=nicecx.get_name())

    def get_sorted_nodes(self, reverse=True):
        # get the nodes as a list, sorted by degree with the highest degree node first.
        return sorted(self.node_dict.values(), key=itemgetter('degree'), reverse=reverse)

    def get_nodecount(self):
        return len(self.node_dict.values())

    def place_nodes_randomly(self, dimension):
        # randomly place the nodes in the center of the board
        for node_id, node in self.node_dict.items():
            self.place_one_node_randomly(node)

    def place_one_node_randomly(self, node, dimension):
        # TODO error if you can't place the node
        center_left = round(dimension / 4)
        center_right = dimension - center_left
        placed = False
        while not placed:
            x = randint(center_left, center_right)
            y = randint(center_left, center_right)
            if not self.node_at_position(x, y):
                node["x"] = x
                node["y"] = y
                placed = True

    def node_at_position(self, x, y):
        for node_id, node in self.node_dict.items():
            if node.get("x") and x == node["x"] and node.get("y") and y == node["y"]:
                return True
        return False

    def place_nodes_at_center(self, center):
        for node_id, node in self.node_dict.items():
            node["x"] = center
            node["y"] = center

    def make_spiral(self, n, center):
        x_list = [center]
        y_list = [center]
        x_dist = 1
        y_dist = 1
        x_dir = 1
        y_dir = 1
        x = center
        y = center
        count = 1
        while count <= n:
            for dx in range(1, x_dist):
                x = x + x_dir
                x_list.append(x)
                y_list.append(y)

                count = count + 1
                if count > n:
                    break
            x_dir = -x_dir
            x_dist = x_dist + 1
            for dy in range(1, y_dist):
                y = y + y_dir
                x_list.append(x)
                y_list.append(y)
                count = count + 1
                if count > n:
                    break
            y_dir = -y_dir
            y_dist = y_dist + 1
        return list(zip(x_list, y_list))

    def place_nodes_in_a_spiral(self, center, scale=1, min_degree=2):
        # This layout ensures that no node is on top of
        # each other and that they are spaced away from
        # each other according to the scaling factor.
        # (the default, 1 = no scaling)
        # This prevents 16-bit overflow due to the center "spike"
        # of the repulsion
        sorted_nodes = self.get_sorted_nodes(reverse=False)
        coordinates = self.make_spiral(len(sorted_nodes), center)
        for index in range(len(sorted_nodes)):
            # start with the low degree nodes in the center
            # the high degree nodes are at the outside.
            # the first layout round will therefore push the
            # high degree nodes out away from the center first,
            # making space for the later parts of the network.
            # The conjecture is that this will improve cluster
            # separation and faster convergence
            node = sorted_nodes[index]
            if node["degree"] >= min_degree:
                node["x"] = coordinates[index][0]
                node["y"] = coordinates[index][1]

    def get_cx_layout(self, node_size=40):
        cx_layout = []
        for node_id, node in self.node_dict.items():
            logger.debug('nodeid: ' + str(node_id) + ' node: ' + str(node))
            cx_node = {"node": int(node_id),
                       "x": int(node["x"] * node_size),
                       "y": int(node["y"] * node_size)}
            cx_layout.append(cx_node)
        return cx_layout

    def get_nx_pos(self, node_size=40):
        pos = {}
        for node_id, node in self.node_dict.items():
            logger.debug('nodeid: ' + str(node_id) + ' node: ' + str(node))
            # the y-coordinate is inverted in networkx
            pos[int(node_id)] = [int(node["x"] * node_size), -int(node["y"] * node_size)]
        return pos
