from qfieldlayout import qlayout
from qfieldlayout.qfigures import save_networkx_plot, save_figure_2, save_figure_3, save_figure_4
from ndex2 import create_nice_cx_from_file
from qfieldlayout.qnetwork import edge_array_from_nicecx

# Generate the Layouts
layouts = {}

# Tiny Graph
print("tiny ")
tiny_edges = [["A", "B"], ["B", "C"], ["A", "D"], ["D", "B"]]
layouts["TINY"] = qlayout.QLayout(tiny_edges, sparsity=15,
                                  r_radius=20, r_scale=10,
                                  a_radius=20, a_scale=10, a_base=5,
                                  center_attractor_scale=5)

tiny_result = layouts["TINY"].do_layout(layout_steps=20, convergence_threshold=0.001)
print("time = " + str(layouts["TINY"].layout_time))

# Small Graph
#
# Medium Graph
print("medium ")
medium_cx = create_nice_cx_from_file('TCR signaling in nave CD4 T cells.cx')
medium_edges = edge_array_from_nicecx(medium_cx)

layouts["MEDIUM"] = qlayout.QLayout(medium_edges, sparsity=15,
                                    r_radius=20, r_scale=10,
                                    a_radius=20, a_scale=10, a_base=5,
                                    center_attractor_scale=5)

medium_result = layouts["MEDIUM"].do_layout(layout_steps=20, convergence_threshold=0.001)
print("time = " + str(layouts["MEDIUM"].layout_time))

# Large Graph
print("large")
large_cx = create_nice_cx_from_file('BioPlex 3 - HEK293T beta cell.cx')
large_edges = edge_array_from_nicecx(large_cx)

layouts["LARGE"] = qlayout.QLayout(large_edges, sparsity=15,
                                    r_radius=20, r_scale=10,
                                    a_radius=20, a_scale=10, a_base=5,
                                    center_attractor_scale=5)

large_result = layouts["LARGE"].do_layout(layout_steps=20, convergence_threshold=0.001)
print("time = " + str(layouts["LARGE"].layout_time))

# Very Large Graph
print("very large ")
very_large_cx = create_nice_cx_from_file('BioPlex_3_HEK293T.cx')
very_large_edges = edge_array_from_nicecx(very_large_cx)

layouts["VERY_LARGE"] = qlayout.QLayout(very_large_edges, sparsity=15,
                                    r_radius=20, r_scale=10,
                                    a_radius=20, a_scale=10, a_base=5,
                                    center_attractor_scale=5)

very_large_result = layouts["VERY_LARGE"].do_layout(layout_steps=20, convergence_threshold=0.001)
print("time = " + str(layouts["VERY_LARGE"].layout_time))

# Figure 1
# Example networks

# Figure 2
# Example fields
save_figure_2(layouts["TINY"].g_field)

# Figure 3
# Convergence plot
save_figure_3(layouts, filename="figure_3")

# Figure 4
# Scaling
save_figure_4(layouts, filename="figure_4")






# test_layout.do_layout(layout_steps=20, convergence_threshold=0.001)

# save_networkx_plot(test_layout.network, test_layout.edge_array, filename="temp_networkx_plot", node_size=200)
