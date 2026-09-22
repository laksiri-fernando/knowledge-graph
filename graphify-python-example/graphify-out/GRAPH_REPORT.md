# Graph Report - graphify-python-example  (2026-09-22)

## Corpus Check
- 3 files · ~40 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 1 file(s) not represented in the graph (top: .lock 1)

## Summary
- 6 nodes · 6 edges · 3 communities (0 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec99401a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app.py
- graphify-python-example
- utility.py

## God Nodes (most connected - your core abstractions)
1. `main()` - 3 edges
2. `welcome()` - 2 edges
3. `add()` - 2 edges
4. `graphify-python-example` - 0 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `add()`  [EXTRACTED]
  app.py → utility.py

## Import Cycles
- None detected.

## Communities (3 total, 3 thin omitted)

## Knowledge Gaps
- **1 isolated node(s):** `graphify-python-example`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `app.py` to `utility.py`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Why does `add()` connect `utility.py` to `app.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **What connects `graphify-python-example` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._