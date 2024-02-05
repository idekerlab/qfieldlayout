from qfieldlayout.qfigures import make_example_network_images, \
    get_example_networks, \
    cx_image_to_file, layout_nice_cx_networks, save_cx_networks_with_layouts

nice_cx_networks = get_example_networks("example_networks")

# layout the networks
layouts = layout_nice_cx_networks(nice_cx_networks, sparsity=25)

# write them out with their layouts
save_cx_networks_with_layouts(layouts, "example_networks_with_layouts", scale=35)

# generate the images
for nice_cx in nice_cx_networks:
    cx_image_to_file(nice_cx, filename=f'example_network_images/{nice_cx.get_name()}.png')
