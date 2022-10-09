from qfieldlayout import qlayout
from qfieldlayout.qfigures import save_networkx_plot

edge_array = [["A", "B"], ["B", "C"], ["A", "D"], ["D", "B"]]

test_layout = qlayout.QLayout(edge_array, sparsity=15,
                              r_radius=20, r_scale=10,
                              a_radius=20, a_scale=10, a_base=5,
                              center_attractor_scale=1,
                              make_figures=True)

test_layout.do_layout(layout_steps=20, convergence_threshold=0.001)

save_networkx_plot(test_layout.network, test_layout.edge_array, filename="temp_networkx_plot", node_size=200)

