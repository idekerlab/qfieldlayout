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

    Z  = np.zeros(length)
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            X[x+y] = x
            Y[x+y] = y
            Z[x+y] = array[x,y]
    X, Y = np.meshgrid(X, Y)
    return X, Y, Z


def save_field_figure_3d(r_radius=20, a_radius=20, r_scale=10, a_scale=10, filename="fields_3d"):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    repulsion = repulsion_field(r_radius, r_scale, center_spike=False)
    attraction = attraction_field_2(a_radius, a_scale)
    y_size = 2 * max((r_radius, a_radius)) + 1
    g_field = np.zeros((2*y_size, y_size))
    y_center = max(r_radius, a_radius) + 1
    add_field(repulsion, g_field, y_center, y_center)
    add_field(repulsion, g_field, y_center + y_size, y_center)
    add_field(attraction, g_field, y_center + y_size, y_center)
    X = np.arange(0, g_field.shape[1])
    Y = np.arange(0, g_field.shape[0])
    X, Y = np.meshgrid(X, Y)

    print(X.shape)
    print(Y.shape)
    # Plot the surface.
    surf = ax.plot_surface(X, Y, g_field, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=10)

    ax.set_box_aspect((X.shape[1], X.shape[0], 50))  # xy aspect ratio is 1:1, but stretches z axis

    plt.savefig(filename, dpi=300)
    plt.clf()


def save_layout_convergence_figure(layouts, filename="figure_3"):
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


def save_layout_time_figure(layouts, filename="figure_4"):
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
