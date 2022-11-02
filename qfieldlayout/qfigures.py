import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from matplotlib import rcParams
from qfieldlayout.fields import repulsion_field, attraction_field


def save_figure_2(g_field, filename="figure_2"):
    fig1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    # repulsion
    repulsion = repulsion_field(20, 10, center_spike=False)
    center_x = int(repulsion.shape[0] / 2)
    ax1.plot(repulsion[center_x])
    ax2.set_xlabel('Energy')
    ax2.set_ylabel('Distance')
    # attraction
    attraction = attraction_field(20, 10)
    center_x = int(attraction.shape[0] / 2)
    ax2.plot(attraction[center_x])
    ax2.set_xlabel('Energy')
    ax2.set_ylabel('Distance')
    # g_field
    # sns.heatmap(g_field)
    # save
    plt.savefig(filename)
    plt.clf()


def save_figure_3(layouts, filename="figure_3"):
    #   rcParams['figure.figsize'] = 10, 6
    for name, layout in layouts.items():
        plt.plot(layout.convergence_history)
    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Iterations")
    plt.ylabel("Convergence Score")
    #   plt.legend(loc=1)
    #   plt.yscale('log')
    plt.savefig(filename)
    plt.clf()


def save_figure_4(layouts, filename="figure_4"):
    #   rcParams['figure.figsize'] = 10, 6
    layout_times = []
    layout_edge_counts = []
    for name, layout in layouts.items():
        layout_times.append(layout.layout_time)
        layout_edge_counts.append(len(layout.edge_array))
    plt.plot(layout_edge_counts, layout_times, markersize=40)
    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Number of Edges")
    plt.ylabel("Layout Time in Seconds")
    #   plt.legend(loc=1)
    #   plt.yscale('log')
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
