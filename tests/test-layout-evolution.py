from qfieldlayout.qfigures import cx_image_to_file
from qfieldlayout.qlayout import QLayout
from qfieldlayout.qnetwork import get_sorted_node_list, get_sorted_node_list_2
import ndex2
from qfieldlayout.qnetwork import edge_array_from_nicecx
import os

network_name = "qfield_test_146_359_louvain_colored"

test_evolution_dir = os.path.join(os.getcwd(), "test_evolution_networks")
print(test_evolution_dir)

#network_name = "qfield_test_96_133"
cx = ndex2.create_nice_cx_from_file('bioplex_test_networks/' + network_name + '.cx')

edges = edge_array_from_nicecx(cx)


def export_step_png(nicecx, step_number):
    cx_image_to_file(nicecx, filename=os.path.join(test_evolution_dir, f'{nicecx.get_name()}_{str(step_number)}.png'))


layout = QLayout(edges,
                 sparsity=15,
                 r_radius=20, r_scale=15,
                 a_radius=10, a_scale=15,
                 center_attractor_scale=4,
                 degree_mode=False)
batch_size = 20
batch_count = 0
for step in range(1, 22):
    node_list = get_sorted_node_list_2(layout.network)
    layout.update_node_positions(step, node_list)
    if batch_count == batch_size:
        batch_count = 0
        cx.set_opaque_aspect(ndex2.constants.CARTESIAN_LAYOUT_ASPECT, layout.get_cx_layout(40))
        print(f'step = {step}')
        export_step_png(cx, step)
    else:
        batch_count += 1

# Convergence plot
# save_layout_convergence_figure(layouts, filename="figure_3")

# Figure 4
# Scaling
# save_layout_time_figure(layouts, filename="figure_4")
