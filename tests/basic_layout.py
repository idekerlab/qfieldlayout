from qfieldlayout import layout
import ndex2

nest = ndex2.create_nice_cx_from_file('nest_cell_map.cx')
nest.print_summary()
nest_layout = layout.QFLayout.from_nicecx(nest, initialize_coordinates="spiral", sparsity=30, r_radius=40,
                        a_radius=40, r_scale=7, a_scale=10, center_attractor_scale=0.03)
layout_result = nest_layout.do_layout(rounds=40)
print(layout_result)
nest.set_opaque_aspect(ndex2.constants.CARTESIAN_LAYOUT_ASPECT, layout_result)
upload_message = nest.upload_to("www.ndexbio.org", "dexterpratt", "cytoscaperules")
print(upload_message)
