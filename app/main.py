from fastapi import FastAPI, HTTPException, BackgroundTasks
import uuid
from app import workflows
from app.models import GraphSpec, RunRequest, NodeSpec
from app.graph_engine import create_graph, run_graph_run, GRAPHS, RUNS

app = FastAPI(title="Workflow Engine - Code Review Agent")

@app.post("/graph/create")
async def create_graph_endpoint(spec: GraphSpec):
    gid = create_graph(spec)
    return {"graph_id": gid}

@app.post("/graph/run")
async def run_graph(req: RunRequest, tasks: BackgroundTasks):
    if req.graph_id not in GRAPHS:
        raise HTTPException(404, "Graph not found")

    run_id = str(uuid.uuid4())
    tasks.add_task(run_graph_run, req.graph_id, req.initial_state, req.max_iterations, run_id)
    return {"run_id": run_id, "status": "started"}

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(404, "Run not found")
    return RUNS[run_id]

@app.post("/graph/create/sample_code_review")
async def create_sample():
    nodes = {
        "extract": NodeSpec(name="extract", fn="extract_functions"),
        "complexity": NodeSpec(name="complexity", fn="check_complexity"),
        "detect": NodeSpec(name="detect", fn="detect_issues"),
        "suggest": NodeSpec(
            name="suggest",
            fn="suggest_improvements",
            condition_key="quality_score",
            branches={"true": "END", "false": "complexity"}
        )
    }

    edges = {
        "extract": "complexity",
        "complexity": "detect",
        "detect": "suggest"
    }

    spec = GraphSpec(nodes=nodes, edges=edges, start_node="extract")
    gid = create_graph(spec)
    return {"graph_id": gid}
