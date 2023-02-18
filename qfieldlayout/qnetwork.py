
from itertools import count
import numpy as np
from operator import itemgetter
from random import randint
import logging
import networkx as nx

logger = logging.getLogger(__name__)


def adjacency_network_from_edge_array(edge_array):
    adjacency_network = {}
    for edge in edge_array:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(str(edge[0]) + ' ' + str(edge[1]))

        if edge[0] not in adjacency_network:
            adjacency_network[edge[0]] = {"adj": set(), "energy": {}, "degree": 1, "id": edge[0]}
        adjacency_network[edge[0]]["adj"].add(edge[1])
        adjacency_network[edge[0]]["degree"] = len(adjacency_network[edge[0]]["adj"])

        if edge[1] not in adjacency_network:
            adjacency_network[edge[1]] = {"adj": set(), "energy": {}, "degree": 1, "id": edge[1]}
        adjacency_network[edge[1]]["adj"].add(edge[0])
        adjacency_network[edge[1]]["degree"] = len(adjacency_network[edge[1]]["adj"])
    return adjacency_network


def get_sorted_node_list(adjacency_network):
    return sorted(adjacency_network.values(), key=itemgetter('degree'), reverse=True)


def get_sorted_node_list_2(adjacency_network):
    degree_sorted = sorted(adjacency_network.values(), key=itemgetter('degree'), reverse=True)
    done = set()
    new_sort = []
    for node in degree_sorted:
        if node["id"] not in done:
            new_sort.append(node)
            done.add(node["id"])
        for adj_node_id in node['adj']:
            adj_node = adjacency_network[adj_node_id]
            if adj_node["id"] not in done:
                new_sort.append(adj_node)
                done.add(adj_node["id"])
    if len(degree_sorted) != len(new_sort):
        raise NameError("error - the re-sorted node list is not the same length")
    return new_sort


def edge_array_from_nicecx(nicecx):
    edge_array = np.zeros((len(nicecx.get_edges()), 2), dtype=int)
    logger.debug("edge array: " + str(edge_array.shape))
    i = 0
    for edge_id, edge in nicecx.get_edges():
        edge_array[i, 0] = edge["s"]
        edge_array[i, 1] = edge["t"]
        i += 1
    return edge_array

def edge_list_from_nicecx(nicecx):
    edge_list = []
    for edge_id, edge in nicecx.get_edges():
        edge_list.append((edge["s"],edge["t"]))
    return edge_list

def get_cx_layout(adjacency_network, node_size=40):
    cx_layout = []
    for node_id, node in adjacency_network.items():
        logger.debug('node_id: ' + str(node_id) + ' node: ' + str(node))
        cx_node = {"node": int(node_id),
                   "x": int(node["x"] * node_size),
                   "y": int(node["y"] * node_size)}
        cx_layout.append(cx_node)
    return cx_layout




