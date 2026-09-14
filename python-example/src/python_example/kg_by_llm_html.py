"""Knowledge Graph extraction from unstructured text using Gemini LLM.

Sends raw text to a Gemini model with a structured output schema, then
exports an interactive HTML visualization via Pyvis.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import pyvis.network as pv

from python_example.llm_extract import SAMPLE_TEXT, extract_graph, load_client

STYLE_OPTIONS: dict = {
    "height": "750px",
    "width": "100%",
    "bgcolor": "#222222",
    "font_color": "white",
    "directed": True,
}

PHYSICS_OPTIONS: str = """
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -4000,
      "centralGravity": 0.3,
      "springLength": 150
    }
  }
}
"""


def build_pyvis_network(kg: nx.DiGraph) -> pv.Network:
    """Convert a NetworkX graph into a styled Pyvis network."""
    net = pv.Network(**STYLE_OPTIONS)
    net.from_nx(kg)

    for edge in net.edges:
        relationship = kg.edges[edge["from"], edge["to"]]["relationship"]
        edge.update(
            {
                "label": relationship,
                "font": {"size": 12, "color": "#ff4d4d", "align": "top"},
                "color": "#4ea8de",
                "width": 2,
            }
        )

    net.set_options(PHYSICS_OPTIONS)
    return net


def export_html(kg: nx.DiGraph, output_path: str | Path) -> None:
    """Write an interactive HTML visualization of *kg* to *output_path*."""
    net = build_pyvis_network(kg)
    net.write_html(str(output_path))
    print(f"Success! Open '{output_path}' in any web browser to view, zoom, and pan your graph.")


def main() -> None:
    """Entry point: extract a knowledge graph from sample text and export HTML."""
    client = load_client()
    kg = extract_graph(client, SAMPLE_TEXT)
    export_html(kg, Path.cwd() / "knowledge_graph.html")


if __name__ == "__main__":
    main()