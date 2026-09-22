# A Guide on Knowledge Graphs

This is a guide on knowledge graphs. The example in ./python-example demonstrate a knowledge graphs generated using python and llm. The examples in ./graphify-python-example and ./graphify-uv-python demonstrates graphify based knowledge graphs

## Graphify Guide

### Step 1: Install Graphify
```bash
uv tool install graphifyy
```

### Step 2: Install It Into Your Project
```bash
# inside project directory
graphify install --platform opencode --project
```

### Step 3: Generate Your Knowledge Graph
```bash
# inside OpenCode
/graphify .
```

### Step 4: Verify
```bash
# inside OpenCode

How does a user prompt flow from input through code generation
# or
Explain how authentication flows through the application.
```

### Step 5: Update Knowledge Graph
```bash
# in terminal
graphify update .
```

## Reference

- [Building a Self-Updating Knowledge Graph for AI Coding Agents](https://niravshah2705.medium.com/building-a-self-updating-knowledge-graph-for-ai-coding-agents-049e889fcdcc)