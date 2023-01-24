import ndex2
import os
from qfieldlayout import qnetwork
import louvain
import igraph
import pandas as pd


def get_network(network_name, subdir=None):
    if subdir:
        network_path = os.path.join(os.getcwd(), subdir, network_name)
    else:
        network_path = os.path.join(os.getcwd(), network_name)
    cx = ndex2.create_nice_cx_from_file(network_path)
    return cx, qnetwork.edge_array_from_nicecx(cx)


def igraph_from_nice_cx(nice_cx):
    g = igraph.Graph(len(nice_cx.get_nodes()))
    # network attributes
    for name in nice_cx.get_network_attribute_names():
        value = nice_cx.get_network_attribute(name)["v"]
        # print(value)
        g[name] = value
        # attribute declarations
    # nodes and attributes and coordinates
    # make a node_id list
    node_id_list = []
    n_id = 0
    for node_id, node in nice_cx.get_nodes():
        g.vs[n_id]["cx_id"] = node_id
        g.vs[n_id]["name"] = node.get('n')
        atts = nice_cx.get_node_attributes(node_id)
        for att in atts:
            att_name = att["n"]
            att_value = att["v"]
            g.vs[n_id][att_name] = att_value
        n_id += 1

    # edges and attributes
    for edge_id, edge in nice_cx.get_edges():
        cx_source_id = edge["s"]
        cx_target_id = edge["t"]
        g_source = g.vs.find(cx_id=cx_source_id)
        g_target = g.vs.find(cx_id=cx_target_id)
        g.add_edges([(g_source, g_target)])
        e_id = g.get_eid(g_source, g_target)
        g.es[e_id]["cx_id"] = edge_id
        atts = nice_cx.get_edge_attributes(node_id)
        if atts is not None:
            for att in atts:
                att_name = att["n"]
                att_value = att["v"]
                g.es[e_id][att_name] = att_value

    # cartesian coordinates
    g["cartesian_layout"] = nice_cx.get_opaque_aspect(ndex2.constants.CARTESIAN_LAYOUT_ASPECT)
    # visual styles
    # bypasses
    # rules
    return g


def get_nice_cx_node_by_key(nice_cx, key, value):
    for node_id, node in nice_cx.get_nodes():
        if node.get(key) == value:
            return node


def df_from_igraph_vertices(g, key, attributes):
    if attributes is None:
        raise RuntimeError("attributes must be a list of one or more attribute names.")
    attributes.insert(0, key)
    zip_list = []
    for attribute in attributes:
        zip_list.append(g.vs[attribute])
    df = pd.DataFrame(zip_list).transpose()
    df.columns = attributes
    print(df.head())
    return df


def merge_igraph_to_nice_cx(g, nice_cx, igraph_key="name", nice_cx_key="n", attributes=None):  # only nodes for now
    vertex_df = df_from_igraph_vertices(g, igraph_key, attributes)
    for index, row in vertex_df.iterrows():
        nice_cx_node = get_nice_cx_node_by_key(nice_cx, nice_cx_key, row[igraph_key])
        for attribute in attributes:
            nice_cx.set_node_attribute(nice_cx_node, attribute, row[attribute])


def cluster_nice_cx(nice_cx):
    g = igraph_from_nice_cx(nice_cx)
    partition = louvain.find_partition(g, louvain.ModularityVertexPartition)

    for i in range(len(partition)):
        members = partition[i]
        for member in members:
            node = (g.vs[member])
            g.vs[member]["cluster"] = i
    merge_igraph_to_nice_cx(g, nice_cx, attributes=["cluster"])
