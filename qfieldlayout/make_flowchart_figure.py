import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add the nodes to the graph
G.add_node('Inputs')
G.add_node('Instantiate Layout object')
G.add_node('Create adjacency list\n dictionary')
G.add_node('Create NumPy arrays\n for fields')
G.add_node('Initialize f-field')
G.add_node('Initialize r-field')
G.add_node('Initialize a-field')
G.add_node('Perform layout')
G.add_node('Outputs')

# Add the edges to the graph
G.add_edge('Inputs', 'Instantiate Layout object')
G.add_edge('Instantiate Layout object', 'Create adjacency list\n dictionary')
G.add_edge('Create adjacency list\n dictionary', 'Create NumPy arrays\n for fields')
G.add_edge('Create NumPy arrays\n for fields', 'Initialize f-field')
G.add_edge('Initialize f-field', 'Initialize r-field')
G.add_edge('Initialize r-field', 'Initialize a-field')
G.add_edge('Initialize a-field', 'Perform layout')
G.add_edge('Perform layout', 'Outputs')

# Set the positions of the nodes
pos = {'Inputs': (0, 3),
       'Instantiate Layout object': (1, 2),
       'Create adjacency list\n dictionary': (2, 1),
       'Create NumPy arrays\n for fields': (3, 2),
       'Initialize f-field': (4, 3),
       'Initialize r-field': (4, 1),
       'Initialize a-field': (4, -1),
       'Perform layout': (5, 0),
       'Outputs': (6, 1)}

# Set the node shape and font size
node_shape = 's' # round rectangle
node_size = 1500
node_font_size = 9

# Draw the nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_shape=node_shape, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, width=10)
nx.draw_networkx_labels(G, pos, font_size=node_font_size, font_family='sans-serif')

# Set the axis limits and remove the axis ticks
plt.xlim(-1, 7)
plt.ylim(-2, 4)
plt.xticks([])
plt.yticks([])

# Show the plot
plt.show()
