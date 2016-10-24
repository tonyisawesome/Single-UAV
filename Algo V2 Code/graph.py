import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()
edges = [(0, 1, 3), (0, 2, 5), (1, 0, 3), (1, 2, 3), (2, 0, 5), (2, 1, 3)]

for start, end, flight_time in edges:
    # You can attach any attributes you want when adding the edge
    G.add_edge(start, end, flight_time=flight_time)

pos = nx.spring_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos,
                       nodelist=[0, 1, 2],
                       node_color='b',
                       node_size=500,
                       alpha=0.8)

nx.draw_networkx_nodes(G, pos,
                       nodelist=[1],
                       node_color='r',
                       node_size=500,
                       alpha=0.8)
# edges
nx.draw_networkx_edges(G, pos,
                       edge_color='black',
                       width=2.0,
                       alpha=0.5,
                       arrows=False)

nx.draw_networkx_edges(G, pos,
                       edgelist=[(2, 1), (1, 2), (2, 0), (0, 2)],
                       edge_color='r',
                       width=2.0,
                       alpha=0.5,
                       style='dashed',
                       arrows=True)

# labels
node_labels = {}
node_labels[0] = r'$0$'
node_labels[1] = r'$1$'
node_labels[2] = r'$2$'
nx.draw_networkx_labels(G, pos, node_labels, font_size=16)
nx.draw_networkx_edge_labels(G, pos, font_size=10)

plt.axis('off')
plt.show()