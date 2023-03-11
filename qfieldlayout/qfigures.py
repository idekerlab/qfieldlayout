import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import seaborn as sns
import networkx as nx
from matplotlib import rcParams
from qfieldlayout.fields import repulsion_field, attraction_field, blank_field, add_field, attraction_field_2
import os
import sys
import json
import time
import requests
import ndex2
import numpy as np
from ndex2 import create_nice_cx_from_file
from qfieldlayout.qnetwork import edge_array_from_nicecx
from qfieldlayout.qlayout import QLayout

# REST_ENDPOINT = 'http://localhost:8081/cd/cd/v1'
REST_ENDPOINT = 'http://cd.ndexbio.org/cd/communitydetection/v1'
HEADERS = {'Content-Type': 'application/json',
           'Accept': 'application/json'}


def cx_image_to_file(nice_cx, width='2048', height='2048', filename="cx_image_default"):
    print('making request to run image export')
    res = requests.post(REST_ENDPOINT,
                        headers=HEADERS,
                        json={'algorithm': 'cytojsimageexport',
                              'customParameters': {'--width': width, '--height': height},
                              'data': nice_cx.to_cx()},
                        timeout=30)
    if res.status_code != 202:
        raise Exception('Error submitting image export task ' + str(res.status_code) + ' : ' + str(res.text))
    task_id = res.json()['id']
    print('Task id is: ' + str(task_id))

    # need to make GET request with task id to check job status
    res = requests.get(REST_ENDPOINT + '/raw/' + str(task_id))

    if res.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)
        print('Output written to: ' + filename)
    else:
        print('Non 200 status code received: ' + str(res.status_code))


def save_field_figure(r_radius=20, a_radius=20, r_scale=10, a_scale=10, filename="figure_2"):
    fig1, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
    # repulsion
    repulsion = repulsion_field(r_radius, r_scale, center_spike=False)
    center_repulsion = int(repulsion.shape[0] / 2)
    ax1.plot(repulsion[center_repulsion])
    ax1.set_xlabel('Distance')
    ax1.set_ylabel('Energy')
    ax1.set_title("r_field")

    # attraction
    attraction = attraction_field_2(a_radius, a_scale)
    center_attraction = int(attraction.shape[0] / 2)
    ax2.plot(attraction[center_attraction])
    ax1.set_xlabel('Distance')
    ax1.set_ylabel('Energy')
    ax2.set_title("a_field")

    # combined
    combined = blank_field(max(r_radius, a_radius))
    center_combined = int(repulsion.shape[0] / 2)
    add_field(repulsion, combined, center_combined, center_combined)
    add_field(attraction, combined, center_combined, center_combined)
    ax3.plot(combined[center_combined])
    ax1.set_xlabel('Distance')
    ax1.set_ylabel('Energy')
    ax3.set_title("combined")
    # g_field
    # sns.heatmap(g_field)
    # save
    plt.savefig(filename)
    plt.clf()


def array_to_coordinate_values(array):
    length = array.shape[0] * array.shape[1]

    Z = np.zeros(length)
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            X[x + y] = x
            Y[x + y] = y
            Z[x + y] = array[x, y]
    X, Y = np.meshgrid(X, Y)
    return X, Y, Z


def save_field_figure_3d(r_radius=20, a_radius=20, r_scale=10, a_scale=10, filename="fields_3d"):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    repulsion = repulsion_field(r_radius, r_scale, center_spike=False)
    attraction = attraction_field_2(a_radius, a_scale)
    y_size = 2 * max((r_radius, a_radius)) + 1
    g_field = np.zeros((2 * y_size, y_size))
    y_center = max(r_radius, a_radius) + 1
    add_field(repulsion, g_field, y_center, y_center)
    add_field(repulsion, g_field, y_center + y_size, y_center)
    add_field(attraction, g_field, y_center + y_size, y_center)
    x = np.arange(0, g_field.shape[1])
    y = np.arange(0, g_field.shape[0])
    x, y = np.meshgrid(x, y)

    print(x.shape)
    print(y.shape)
    # Plot the surface.
    surf = ax.plot_surface(x, y, g_field, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=10)

    fig.tight_layout(pad=2.0)

    ax.set_box_aspect((x.shape[1], x.shape[0], 50))  # xy aspect ratio is 1:1, but stretches z axis

    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.clf()


def save_layout_convergence_figure(layout_stats, filename="convergence_figure", network_names=None):
    if network_names is None:
        for layout in layout_stats:
            plt.plot(layout['convergence_history'], label=layout['network_name'])
    else:
        for layout in layout_stats:
            if layout['network_name'] in network_names:
                plt.plot(layout['convergence_history'],
                         label=parse_test_network_name_to_counts(layout['network_name']))
    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Iterations")
    plt.ylabel("Convergence Score")
    plt.legend()
    plt.savefig(filename)
    plt.clf()


def parse_test_network_name_to_counts(s):
    # split the string into parts
    parts = s.split("_")

    # extract the node and edge counts
    nodes = parts[2]
    edges = parts[3]

    # create the formatted string
    return "nodes: {}, edges: {}".format(nodes, edges)

'''
def save_layout_time_figure(layouts, filename="figure_4"):
    layout_times = []
    layout_edge_counts = []
    for name, layout in layouts.items():
        layout_times.append(layout['layout_time'])
        layout_edge_counts.append(len(layout['edge_array']))
    plt.plot(layout_edge_counts, layout_times, markersize=40)
    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Number of Edges")
    plt.ylabel("Layout Time in Seconds")
    #   plt.legend(loc=1)
    #   plt.yscale('log')
    plt.savefig(filename)
    plt.clf()
'''


def save_layout_iteration_time_figure(layout_stats, filename="layout_iteration_time_figure"):
    iteration_times = []
    layout_edge_node_counts = []
    for layout in layout_stats:
        print(layout)
        print(layout['convergence_history'])
        number_of_iterations = len(layout['convergence_history']) + 1
        print(number_of_iterations)
        average_iteration_time = layout['layout_time'] / number_of_iterations
        iteration_times.append(average_iteration_time)
        layout_edge_node_counts.append(int(layout['edge_count'] + (2 * layout['node_count'])))

    plt.loglog(layout_edge_node_counts, iteration_times, 'o', label='Data')

    plt.gca().xaxis.set_major_formatter(plt.LogFormatter(base=10))
    plt.gca().yaxis.set_major_formatter(plt.LogFormatter(base=10))

    # Set the tick label formatter
    plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False))
    plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False))

    # Set the tick locations to powers of 10
    plt.xticks([10 ** i for i in range(1, 6)])
    plt.yticks([10 ** i for i in range(-2, 2)])

    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Number of Edges + 2 * Number of Nodes")
    plt.ylabel("Layout Iteration Time in Seconds")
    #   plt.legend(loc=1)
    #   plt.yscale('log')
    plt.savefig(filename)
    plt.clf()


def save_layout_iteration_size_figure(layout_stats, filename="layout_iteration_size_figure"):
    iteration_numbers = []
    layout_edge_node_counts = []
    for layout in layout_stats:
        number_of_iterations = len(layout['convergence_history']) + 1
        iteration_numbers.append(number_of_iterations)
        layout_edge_node_counts.append(int(layout['edge_count'] + (2 * layout['node_count'])))
        # layout_edge_counts.append(layout['edge_count'])

    plt.plot(layout_edge_node_counts, iteration_numbers, 'o', label='Data')

    plt.xscale('log')

    plt.gca().xaxis.set_major_formatter(plt.LogFormatter(base=10))

    # Set the tick label formatter
    plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False))

    # Set the tick locations to powers of 10
    plt.xticks([10 ** i for i in range(1, 6)])

    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Number of Edges + 2 * Number of Nodes")
    plt.ylabel("Number of Iterations")

    plt.savefig(filename)
    plt.clf()


def save_layout_iteration_node_degree_figure(layout_stats, filename="layout_iteration_node_degree_figure"):
    iteration_numbers = []
    layout_node_degrees = []
    for layout in layout_stats:
        number_of_iterations = len(layout['convergence_history']) + 1
        iteration_numbers.append(number_of_iterations)
        layout_node_degrees.append(layout['average_degree'])

    plt.plot(layout_node_degrees, iteration_numbers, 'o', label='Data')
    # plt.xscale('log')

    # plt.gca().xaxis.set_major_formatter(plt.LogFormatter(base=10))

    # Set the tick label formatter
    # plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False))

    # Set the tick locations to powers of 10
    # plt.xticks([10 ** i for i in range(1, 6)])

    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Average Node Degree")
    plt.ylabel("Layout Iteration Time in Seconds")

    plt.savefig(filename)
    plt.clf()


def process_test_networks(input_network_folder, output_network_folder, scale=40):
    nice_cx_networks = get_test_networks(input_network_folder)
    layouts = layout_nice_cx_networks(nice_cx_networks)
    stats_list = make_stats_list(layouts)
    with open('layout_stats.json', 'w') as outfile:
        json.dump(stats_list, outfile)
    save_cx_networks_with_layouts(layouts, output_network_folder, scale=scale)


def get_test_networks(input_network_folder):
    nice_cx_networks = []
    for filename in os.listdir(input_network_folder):
        if filename.endswith('.cx'):
            filepath = os.path.join(input_network_folder, filename)
            if os.path.isfile(filepath):
                nice_cx_network = create_nice_cx_from_file(filepath)
                nice_cx_networks.append(nice_cx_network)
    return nice_cx_networks


def layout_nice_cx_networks(nice_cx_networks):
    layouts = []
    for nice_cx_network in nice_cx_networks:
        edge_array = edge_array_from_nicecx(nice_cx_network)
        layout = QLayout(edge_array, sparsity=15, r_radius=20, r_scale=15, a_radius=10, a_scale=15,
                         center_attractor_scale=4, degree_mode=False)
        layout.do_layout(convergence_threshold=0.0001)
        print(nice_cx_network.get_name())
        layouts.append([layout, nice_cx_network])
    return layouts


def make_stats_list(layouts):
    stats_list = []
    for layout_and_network in layouts:
        layout = layout_and_network[0]
        nice_cx = layout_and_network[1]
        networkx_graph = nice_cx.to_networkx()

        stats_dict = {}
        stats_dict['network_name'] = nice_cx.get_name()

        degree_sum = 0
        for item in networkx_graph.degree():
            degree_sum += item[1]
        stats_dict['average_degree'] = degree_sum / len(networkx_graph)

        stats_dict['node_count'] = len(networkx_graph)
        stats_dict['layout_time'] = layout.layout_time
        stats_dict['convergence_history'] = layout.convergence_history
        stats_dict['edge_count'] = len(layout.edge_array)
        stats_list.append(stats_dict)
    return stats_list


def save_cx_networks_with_layouts(layouts, output_network_folder, scale=40):
    for layout_and_network in layouts:
        layout = layout_and_network[0]
        nice_cx_network = layout_and_network[1]
        nice_cx_network.set_opaque_aspect(ndex2.constants.CARTESIAN_LAYOUT_ASPECT, layout.get_cx_layout(scale))
        cx = nice_cx_network.to_cx()
        path = os.path.join(output_network_folder, nice_cx_network.get_name()) + ".cx"
        with open(path, 'w') as outfile:
            json.dump(cx, outfile)


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
