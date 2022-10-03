from qfieldlayout import qlayout
from qfieldlayout import fields
import ndex2
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

g = ndex2.create_nice_cx_from_file('TCR signaling in nave CD4 T cells.cx')
#g = ndex2.create_nice_cx_from_file('nest_cell_map.cx')
# g = ndex2.create_nice_cx_from_file('BioPlex 3 - HEK293T beta cell.cx')
g_nx = g.to_networkx(mode='default')
#nest = ndex2.create_nice_cx_from_file('nest_cell_map.cx')
g.print_summary()
g_layout = qlayout.QLayout.from_nicecx(g, sparsity=15, r_radius=20,
                        a_radius=20, r_scale=10, a_scale=10, a_base=5, center_attractor_scale=1)
layout_result = g_layout.do_layout(rounds=20, threshold = 0.001)



print(g_layout.alpha)
plt.yscale('log')
plt.plot(g_layout.alpha)
plt.show()
#fields.remove_spikes(g_layout.gfield, max = 1000)
#sns.heatmap(g_layout.gfield)
nx.draw(g_nx,g_layout.network.get_nx_pos(100), node_size=10)
plt.show()
