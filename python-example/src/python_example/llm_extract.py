"""Shared LLM knowledge-graph extraction logic.

Provides the structured output schema, an authenticated Gemini client
factory, and a function that turns unstructured text into a NetworkX
directed graph. Imported by the plotting and HTML-export example scripts.
"""

from __future__ import annotations

import os
from pathlib import Path

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

PROMPT_TEMPLATE: str = (
    "Analyze the following text and extract a comprehensive knowledge graph. "
    "Identify the key people, places, concepts, or objects as nodes, and determine how they connect.\n\n"
    "Text to analyze:\n{text}"
)


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
    print("Sending text to Gemini ...")
    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=KnowledgeGraphSchema,
            temperature=0.1,
        ),
    )
    response = chat.send_message(PROMPT_TEMPLATE.format(text=text))

    if not response.text:
        raise RuntimeError("Gemini returned an empty response. Check your API key and safety settings.")

    data = KnowledgeGraphSchema.model_validate_json(response.text)

    kg: nx.DiGraph = nx.DiGraph()
    for edge in data.connections:
        kg.add_edge(edge.source, edge.target, relationship=edge.relationship)
        print(f"  [{edge.source}] --({edge.relationship})--> [{edge.target}]")

    return kg
