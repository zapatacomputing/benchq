import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D


def plot_graph_state(asg, pauli_tracker):
    """Converts an adjacency list to an adjacency matrix.

    Args:
      adj: The adjacency list to convert.

    Returns:
      The adjacency matrix.
    """
    adj, lco, input_nodes, output_nodes = (
        asg["edge_data"],
        asg["sqs"],
        asg["stitching_properties"]["graph_input_nodes"],
        asg["stitching_properties"]["graph_output_nodes"],
    )

    plt.subplot(1, 2, 1)
    plt.title("Graph State")

    # Create the adjacency matrix.
    adjacency_matrix = [[0 for _ in range(len(adj))] for _ in range(len(adj))]

    # Iterate over the adjacency list and fill in the adjacency matrix.
    for node, neighbors in enumerate(adj):
        for neighbor in neighbors:
            adjacency_matrix[node][neighbor] = 1

    graph = nx.from_numpy_matrix(np.array(adjacency_matrix))

    # Remove isolated nodes
    # isolated_nodes = [
    #     node for node, degree in dict(graph.degree()).items() if degree == 0
    # ]
    # graph.remove_nodes_from(isolated_nodes)

    # Create a legend for node colors
    spacial_node_colors = {
        "I": "grey",
        "S": "lime",
        "H": "red",
        "HSH": "magenta",
        "HS": "cyan",
        "SH": "orange",
    }
    legend_patches = [
        mpatches.Patch(color=color, label=node)
        for node, color in spacial_node_colors.items()
    ]

    # Plot a graph with lco labels
    color_map = []
    for node, lco in enumerate(lco):
        if lco == 1:
            color_map.append(spacial_node_colors["I"])
        elif lco == 2:
            color_map.append(spacial_node_colors["S"])
        elif lco == 3:
            color_map.append(spacial_node_colors["H"])
        elif lco == 4:
            color_map.append(spacial_node_colors["HSH"])
        elif lco == 5:
            color_map.append(spacial_node_colors["HS"])
        elif lco == 6:
            color_map.append(spacial_node_colors["SH"])
        else:
            raise ValueError(f"lco {lco} not supported.")

    legend_patches += [
        Line2D(
            [0],
            [0],
            marker="s",
            color="black",
            label="Input",
            markerfacecolor="w",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="black",
            label="Intermediate",
            markerfacecolor="w",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="d",
            color="black",
            label="Output",
            markerfacecolor="w",
            markersize=10,
        ),
    ]

    plt.legend(handles=legend_patches, loc="upper right")
    for node in graph.nodes:
        if node in input_nodes:
            graph.nodes[node]["shape"] = "s"
        elif node in output_nodes:
            graph.nodes[node]["shape"] = "d"
        else:
            graph.nodes[node]["shape"] = "o"

    # Drawing the graph
    # First obtain the node positions using one of the layouts
    nodePos = nx.layout.spring_layout(graph)

    # The rest of the code here attempts to automate the whole process by
    # first determining how many different node classes (according to
    # attribute 's') exist in the node set and then repeatedly calling
    # draw_networkx_node for each. Perhaps this part can be optimized further.

    # Get all distinct node classes according to the node shape attribute
    nodeShapes = set((aShape[1]["shape"] for aShape in graph.nodes(data=True)))

    # For each node class...
    for aShape in nodeShapes:
        # ...filter and draw the subset of nodes with the same symbol in the positions
        # that are now known through the use of the layout.
        nodes_with_this_shape = [
            sNode[0]
            for sNode in filter(
                lambda x: x[1]["shape"] == aShape, graph.nodes(data=True)
            )
        ]
        colors_for_nodes_with_this_shape = [
            color_map[i] for i in nodes_with_this_shape if 0 <= i < len(color_map)
        ]

        nx.draw_networkx_nodes(
            graph,
            nodePos,
            node_shape=aShape,
            nodelist=nodes_with_this_shape,
            node_color=colors_for_nodes_with_this_shape,
            node_size=120,
        )
    nx.draw_networkx_labels(graph, nodePos)

    # Finally, draw the edges between the nodes
    nx.draw_networkx_edges(graph, nodePos)

    # create graph for pauli flow
    plt.subplot(1, 2, 2)
    plt.title("Pauli Flow")
    x_pauli_flow = nx.DiGraph()
    z_pauli_flow = nx.DiGraph()

    # Add node
    # s and edges from the adjacency list
    for node, neighbors in enumerate(pauli_tracker["cond_paulis"]):
        x_pauli_flow.add_node(node)
        z_pauli_flow.add_node(node)
        for neighbor in neighbors[0]:
            x_pauli_flow.add_edge(neighbor, node, color="red")
        for neighbor in neighbors[1]:
            z_pauli_flow.add_edge(neighbor, node, color="blue")

    x_temporal_edge_colors = [
        x_pauli_flow[u][v]["color"] for u, v in x_pauli_flow.edges()
    ]
    z_temporal_edge_colors = [
        z_pauli_flow[u][v]["color"] for u, v in z_pauli_flow.edges()
    ]

    # Create positions based on layering
    pos = {}
    for i, layer in enumerate(pauli_tracker["layering"]):
        for j, node in enumerate(layer):
            pos[node] = (
                j,
                -i,
            )  # Adjust the y-coordinate for vertical spacing

    # Plot the graph
    nx.draw(
        x_pauli_flow,
        pos,
        edge_color=x_temporal_edge_colors,
        with_labels=True,
        arrows=True,
        connectionstyle="arc3,rad=0.2",
    )
    nx.draw(
        z_pauli_flow,
        pos,
        edge_color=z_temporal_edge_colors,
        with_labels=True,
        arrows=True,
        connectionstyle="arc3,rad=-0.2",
    )

    # Add dashed lines between layers
    max_layer_width = max([len(layer) for layer in pauli_tracker["layering"]])
    for layer_index in range(1, len(pauli_tracker["layering"])):
        plt.plot(
            [-0.5, max_layer_width - 0.5],
            [-layer_index + 0.5, -layer_index + 0.5],
            "k--",
            lw=1,
            alpha=0.5,
        )

    plt.tight_layout()
    # Create a legend
    red_patch = plt.Line2D(
        [0], [0], marker="o", color="w", markerfacecolor="red", markersize=8, label="X"
    )
    blue_patch = plt.Line2D(
        [0], [0], marker="o", color="w", markerfacecolor="blue", markersize=8, label="Z"
    )

    # Display the legend
    plt.legend(handles=[red_patch, blue_patch], loc="lower right")

    plt.show()

    return graph
