from qfieldlayout import qlayout
from qfieldlayout import qtests

from qfieldlayout import fields
from qfieldlayout.qnetwork import edge_array_from_nicecx
import ndex2
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from qfieldlayout.qfigures import cx_image_to_file
import os
import numpy as np

UPLOAD = True
PLOT = False

network, edges = qtests.get_network("qfield_test_96_133.cx", subdir="bioplex_test_networks")
# network, edges = get_network("TCR signaling in nave CD4 T cells.cx", subdir="misc_test_networks")
layout = qlayout.QLayout(edges,
                         sparsity=10,
                         r_radius=10, r_scale=10,
                         a_radius=20, a_scale=20,
                         a_base=0,
                         center_attractor_scale=5)

layout.do_layout(layout_steps=20, convergence_threshold=0.001)
print("layout time = " + str(layout.layout_time))

network.set_opaque_aspect(ndex2.constants.CARTESIAN_LAYOUT_ASPECT, layout.get_cx_layout(60))

# set the description to include all of the parameters, timing, convergence...
# network.set_description("")
if UPLOAD:
    upload_message = network.upload_to("www.ndexbio.org", "dexterpratt", "cytoscaperules")
    print(upload_message.replace("/v2/network", "/viewer/networks"))
else:
    cx_image_to_file(network, filename=f'{network.get_name()}_test.png')

# def plot_convergence(layout): #, filename="figure_3"):
#   rcParams['figure.figsize'] = 10, 6
print(f'{*layout.convergence_history,}')
if PLOT:
    plt.plot(layout.convergence_history)
    plt.grid(True, color='k', linestyle=':')
    plt.xlabel("Iterations")
    plt.ylabel("Convergence Score")
    #   plt.legend(loc=1)
    #   plt.yscale('log')
    plt.show()

print([np.amin(x) for x in layout.a_fields.values()])
# plot_convergence(layout)
