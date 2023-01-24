from qfieldlayout.qfigures import cx_image_to_file
import ndex2
from qfieldlayout.qnetwork import edge_array_from_nicecx
import os
import glob


def get_network(network_name):
    cx = ndex2.create_nice_cx_from_file('bioplex_test_networks/' + network_name + '.cx')
    return cx, edge_array_from_nicecx(cx)

cwd = os.getcwd()
test_network_dir = os.path.join(cwd, "bioplex_test_networks")
print(test_network_dir)
for filename in glob.glob(os.path.join(test_network_dir, '*.cx')):
    path = os.path.join(test_network_dir, filename)
    print(f'filename = {filename} path = {path}')
    network = ndex2.create_nice_cx_from_file(path)
    if len(network.edges) < 1000:
        cx_image_to_file(network, filename=os.path.join(test_network_dir, f'{network.get_name()}.png'))
