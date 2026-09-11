"""Knowledge Graph extraction from unstructured text using Gemini LLM.

Sends raw text to a Gemini model with a structured output schema, then
builds and visualizes the resulting knowledge graph with NetworkX.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

MODEL_NAME: str = "gemini-3.6-flash"

SAMPLE_TEXT: str = """\
Alan Turing was a brilliant British mathematician who made foundational contributions to computer science. \
He designed the concept of the Turing Machine, which directly influenced the creation of the Modern Computer. \
During World War II, Turing worked closely with Joan Clarke at Bletchley Park. \
Together, they cracked the Enigma Code, which helped the Allies win the war.
"""


class Edge(BaseModel):
    """A single directed relationship between two entities."""

    source: str = Field(description="The starting entity (node) of the relationship.")
    target: str = Field(description="The target entity (node) of the relationship.")
    relationship: str = Field(description="The verb or connection phrase explaining how source relates to target.")


class KnowledgeGraphSchema(BaseModel):
    """Structured output schema for LLM-extracted knowledge graph connections."""

    connections: list[Edge] = Field(description="A list of all extracted entity relationships.")


def load_client() -> genai.Client:
    """Load environment variables and return an authenticated Gemini client."""
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Create a .env file with your key "
            f"(see .env.example). Searched: {env_path}"
        )

    return genai.Client(api_key=api_key)


def extract_graph(client: genai.Client, text: str) -> nx.DiGraph:
    """Send *text* to Gemini and return a NetworkX DiGraph of the extracted relationships."""
    prompt = (
        "Analyze the following text and extract a comprehensive knowledge graph. "
        "Identify the key people, places, concepts, or objects as nodes, and determine how they connect.\n\n"
        f"Text to analyze:\n{text}"
    )

    print("Sending text to Gemini ...")
    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=KnowledgeGraphSchema,
            temperature=0.1,
        ),
    )
    response = chat.send_message(prompt)

    if not response.text:
        raise RuntimeError("Gemini returned an empty response. Check your API key and safety settings.")

    data = KnowledgeGraphSchema.model_validate_json(response.text)

    kg: nx.DiGraph = nx.DiGraph()
    for edge in data.connections:
        kg.add_edge(edge.source, edge.target, relationship=edge.relationship)
        print(f"  [{edge.source}] --({edge.relationship})--> [{edge.target}]")

    return kg


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
