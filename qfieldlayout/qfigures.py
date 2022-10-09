import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx


def save_field_cross_section_plot(field, filename="temp_plot.ping"):
    center_x = int(field.shape[0] / 2)
    plt.plot(field[center_x])
    plt.savefig(filename)
    plt.clf()


def save_field_heatmap(field, filename="temp_heatmap"):
    sns.heatmap(field)
    plt.savefig(filename)
    plt.clf()


def save_convergence_graph(convergence_histories, filename="temp_convergence"):
    plt.yscale('log')
    plt.plot(convergence_histories[0])
    plt.savefig(filename)
    plt.clf()


def save_networkx_plot(adjacency_network, edge_array, node_size=40, scale=10, filename="temp_networkx_plot"):
    g = nx.Graph()
    pos = get_nx_pos(adjacency_network, scale=scale)
    for edge in edge_array:
        node_id_1 = adjacency_network[edge[0]]["id"]
        node_id_2 = adjacency_network[edge[1]]["id"]
        g.add_edge(node_id_1, node_id_2)
    nx.draw(g, pos, node_size=node_size)
    plt.savefig(filename)
    plt.clf()


def get_nx_pos(adjacency_network, scale=1):
    pos = {}
    for node_name, node in adjacency_network.items():
        # logger.debug('node_id: ' + str(node["id"]) + ' node: ' + str(node))
        # the y-coordinate is inverted in networkx
        pos[int(node["id"])] = [int(node["x"] * scale), -int(node["y"] * scale)]
    return pos
