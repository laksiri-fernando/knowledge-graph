"""Knowledge Graph example using NetworkX and Matplotlib.

Builds a small directed graph of learning topics, inspects its properties,
and visualizes it.
"""

from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt


def build_graph() -> nx.DiGraph:
    """Build and return a sample knowledge graph of learning topics."""
    kg: nx.DiGraph = nx.DiGraph()

    nodes: list[tuple[str, dict[str, str]]] = [
        ("Python", {"level": "Beginner", "category": "Language"}),
        ("Data Structures", {"level": "Intermediate", "category": "Computer Science"}),
        ("Machine Learning", {"level": "Advanced", "category": "AI"}),
        ("Deep Learning", {"level": "Expert", "category": "AI"}),
    ]
    kg.add_nodes_from(nodes)

    edges: list[tuple[str, str, dict[str, str]]] = [
        ("Python", "Machine Learning", {"relationship": "used_in"}),
        ("Python", "Data Structures", {"relationship": "prerequisite_for"}),
        ("Data Structures", "Machine Learning", {"relationship": "prerequisite_for"}),
        ("Machine Learning", "Deep Learning", {"relationship": "evolved_into"}),
    ]
    kg.add_edges_from(edges)

    return kg


def print_graph_info(kg: nx.DiGraph) -> None:
    """Print summary statistics and sample edge metadata."""
    print(f"Total Nodes: {kg.number_of_nodes()}")
    print(f"Total Edges: {kg.number_of_edges()}")

    rel: str = kg.edges["Python", "Machine Learning"]["relationship"]
    print(f"Relationship between Python and Machine Learning: {rel}\n")


def visualize_graph(kg: nx.DiGraph) -> None:
    """Display a labeled visualization of the knowledge graph."""
    plt.figure(figsize=(10, 7))

    pos = nx.spring_layout(kg, seed=42)

    nx.draw_networkx_nodes(kg, pos, node_size=2000, node_color="skyblue")
    nx.draw_networkx_edges(
        kg, pos, arrowstyle="->", arrowsize=20, edge_color="gray", width=2
    )
    nx.draw_networkx_labels(kg, pos, font_size=10, font_weight="bold")

    edge_labels = nx.get_edge_attributes(kg, "relationship")
    nx.draw_networkx_edge_labels(kg, pos, edge_labels=edge_labels, font_size=9)

    plt.title("Sample Knowledge Graph", fontsize=14)
    plt.axis("off")
    plt.show()


def main() -> None:
    """Entry point: build, inspect, and visualize the knowledge graph."""
    kg = build_graph()
    print_graph_info(kg)
    visualize_graph(kg)


if __name__ == "__main__":
    main()
