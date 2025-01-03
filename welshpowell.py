import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def create_adjacency_matrix_from_list(adj_list):
    nodes = list(adj_list.keys())
    n = len(nodes)
    matrix = np.zeros((n, n), dtype=int)

    node_index = {node: i for i, node in enumerate(nodes)}

    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            matrix[node_index[node]][node_index[neighbor]] = 1
            matrix[node_index[neighbor]][node_index[node]] = 1 

    return matrix, nodes

# Welsh-Powell untuk pewarnaan graf
def welsh_powell(graph):
    sorted_nodes = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)
    colors = {}
    available_colors = []
    for node in sorted_nodes:
        used_colors = {colors[neighbor] for neighbor in graph[node] if neighbor in colors}
        for color in available_colors:
            if color not in used_colors:
                colors[node] = color
                break
        else:
            new_color = len(available_colors) + 1
            colors[node] = new_color
            available_colors.append(new_color)
    return colors

adj_list = {
    "Room A": ["Room C", "Room D"],
    "Room B": ["Room D", "Room E"],
    "Room C": ["Room A", "Room B"],
    "Room D": ["Room C", "Room A"],
    "Room E": ["Room A", "Room D", "Room B"],
    }

adj_matrix, nodes = create_adjacency_matrix_from_list(adj_list)
adj_matrix_df = pd.DataFrame(adj_matrix, index=nodes, columns=nodes)

graph = {node: [] for node in nodes}
for i, node1 in enumerate(nodes):
    for j, node2 in enumerate(nodes):
        if adj_matrix[i][j] == 1:
            graph[node1].append(node2)

colors = welsh_powell(graph)

min_cctv = max(colors.values())

print("Adjacency Matrix:")
print(adj_matrix_df)


print(f"\nMinimum CCTV needed: {min_cctv}")


print("\nColor for every room:")
for room, color in colors.items():
    print(f"- {room}: Color {color}")

def visualize_colored_graph(graph, colors):
    G = nx.Graph()
   
    for node, neighbors in graph.items():
        G.add_node(node, color=colors[node])
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
  
    node_colors = [colors[node] for node in G.nodes()]

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Set3, node_size=2000, font_size=10)
    plt.title("Colored Room Graph")
    plt.show()

visualize_colored_graph(graph, colors)
