from qfieldlayout import layout
import ndex2
g = ndex2.create_nice_cx_from_file('TCR signaling in nave CD4 T cells.cx')

#nest = ndex2.create_nice_cx_from_file('nest_cell_map.cx')
g.print_summary()
g_layout = layout.QFLayout.from_nicecx(g, initialize_coordinates="spiral", sparsity=15, r_radius=10,
                        a_radius=15, r_scale=7, a_scale=20, center_attractor_scale=0.03, verbose=True)
layout_result = g_layout.do_layout(rounds=20, degree_2_plus_rounds= 10, node_size=100)
print(layout_result)
g.set_opaque_aspect(ndex2.constants.CARTESIAN_LAYOUT_ASPECT, layout_result)
upload_message = g.upload_to("www.ndexbio.org", "dexterpratt", "cytoscaperules")
print(upload_message)
