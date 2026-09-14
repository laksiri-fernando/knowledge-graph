"""Knowledge Graph extraction from unstructured text using Gemini LLM.

Sends raw text to a Gemini model with a structured output schema, then
plots the resulting knowledge graph with NetworkX and Matplotlib.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from python_example.llm_extract import SAMPLE_TEXT, extract_graph, load_client


def visualize_graph(kg: nx.DiGraph) -> None:
    """Display a labeled visualization of the knowledge graph."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(kg, k=1.5, seed=42)

    nx.draw_networkx_nodes(kg, pos, node_size=2500, node_color="#a8dadc")
    nx.draw_networkx_edges(kg, pos, arrowstyle="->", arrowsize=15, edge_color="#1d3557", width=1.5)
    nx.draw_networkx_labels(kg, pos, font_size=9, font_weight="bold")

    edge_labels = nx.get_edge_attributes(kg, "relationship")
    nx.draw_networkx_edge_labels(kg, pos, edge_labels=edge_labels, font_size=8, font_color="#e63946")

    plt.title("LLM-Extracted Knowledge Graph", fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Entry point: extract a knowledge graph from sample text and visualize it."""
    client = load_client()
    kg = extract_graph(client, SAMPLE_TEXT)
    visualize_graph(kg)


if __name__ == "__main__":
    main()