from qfieldlayout.qfigures import save_layout_iteration_time_figure, save_layout_convergence_figure, \
    save_layout_iteration_size_figure, save_layout_iteration_node_degree_figure
import json

with open('layout_stats.json') as f:
    layout_stats = json.load(f)

save_layout_iteration_time_figure(layout_stats)

save_layout_convergence_figure(layout_stats,
                               network_names=["qfield_test_41_93",
                                              "qfield_test_618_1824",
                                              "qfield_test_3K_12K",
                                              "qfield_test_14K_130K"])

save_layout_iteration_size_figure(layout_stats)

save_layout_iteration_node_degree_figure(layout_stats)
