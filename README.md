# Mini Workflow Engine – Code Review Agent

This project implements a small workflow/agent engine (a simplified LangGraph-style system) for the **AI Engineering Intern Assignment**.

It demonstrates:

- Node-based workflows using Python functions (tools)
- Shared state passed across nodes
- Branching and simple looping
- FastAPI endpoints to create/execute graphs
- A complete example agent workflow: **Code Review Mini-Agent**

---

##  Project Contents

| File | Purpose |
|------|---------|
| `app/registry.py` | Tool registry + function execution |
| `app/graph_engine.py` | Graph creation + run loop + in-memory run store |
| `app/models.py` | Pydantic models defining NodeSpec, GraphSpec, RunRequest |
| `app/workflows/code_review.py` | Implementation of agent workflow nodes |
| `app/main.py` | FastAPI endpoints |
| `requirements.txt` | Dependencies |

---

##  Quick Start

### Create a virtual environment and install dependencies

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

###  Start FastAPI server

```bash
uvicorn app.main:app --reload
```

###  Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## How the Workflow Engine Works

This engine executes a directed graph of nodes.  
Each node is a **registered tool** (Python function) that:

- Receives the workflow state
- Mutates the state
- Returns information
- Hands off control to the next node

### Nodes in the Code Review Workflow:

1. **extract_functions**
   - Extracts function names
   - Counts lines + basic complexity markers

2. **check_complexity**
   - Computes a lightweight complexity score

3. **detect_issues**
   - Detects long functions
   - Detects high complexity

4. **suggest_improvements**
   - Generates suggestions
   - Computes `quality_score`
   - Branches:  
     - If score is **truthy** → END  
     - Else → loop to `complexity`

---

## ▶️ Running the Built-in Code Review Workflow

### Create the sample graph:

**POST** `/graph/create/sample_code_review`

Response example:

```json
{"graph_id": "66a29645-e9ac-4851-84e0-3991df5cb2a3"}
```

### Run the workflow:

**POST** `/graph/run`

Example body:

```json
{
  "graph_id": "66a29645-e9ac-4851-84e0-3991df5cb2a3",
  "initial_state": {
    "code": "def add(a, b):\n    return a + b\n"
  },
  "max_iterations": 5
}
```

###  Check final state:

**GET** `/graph/state/{run_id}`

---

##  Sample Output (Shortened)

```json
{
  "state": {
    "functions": [
      {"name": "add", "lines": 2, "complexity": 0}
    ],
    "complexity_score": 1.2,
    "issues": [],
    "quality_score": 98.8
  },
  "log": [
    {"step": 1, "node": "extract"},
    {"step": 2, "node": "complexity"},
    {"step": 3, "node": "detect"},
    {"step": 4, "node": "suggest"}
  ],
  "status": "done"
}
```

---

##  What the Engine Supports

- Node-based execution
- Directed graph with edges
- Branching based on state
- Looping until condition met
- Async background execution
- Execution logs for each step
- Minimal, clean API design

---

##  Improvements If Given More Time

With additional time, I would add:

1. Graph visualization  
2. WebSocket real-time log streaming  
3. AST-based static analysis instead of regex  
4. Parallel execution for independent nodes  
5. Persistent storage for graphs & runs  
6. Optional LLM-powered tools for real code reviews  



## Author

Santhosh Shivam  
AI Engineering Intern Assignment  
Mini Workflow Engine + Code Review Agent
