import uuid
from typing import Dict, Any, Optional, Tuple
from .models import GraphSpec
from .registry import run_tool

GRAPHS: Dict[str, GraphSpec] = {}
RUNS: Dict[str, Dict[str, Any]] = {}

def create_graph(spec: GraphSpec) -> str:
    graph_id = spec.graph_id or str(uuid.uuid4())
    spec.graph_id = graph_id
    GRAPHS[graph_id] = spec
    return graph_id

def get_next_node(spec: GraphSpec, current: str, state: Dict[str, Any]) -> Optional[str]:
    node = spec.nodes[current]

    
    if node.branches and node.condition_key:
        val = state.get(node.condition_key)
        branch_key = "true" if val else "false"
        nxt = node.branches.get(branch_key)

        
        if nxt == "END":
            return None
        return nxt

    
    return spec.edges.get(current)

async def run_graph_run(graph_id: str, initial_state: Dict[str, Any], max_iterations: int = 10, run_id: Optional[str] = None):
    if graph_id not in GRAPHS:
        raise KeyError("Graph not found")

    spec = GRAPHS[graph_id]
    run_id = run_id or str(uuid.uuid4())

    state = dict(initial_state)
    RUNS[run_id] = {"state": state, "log": [], "status": "running"}

    current = spec.start_node
    iteration = 0

    while current and iteration < max_iterations:
        iteration += 1

        RUNS[run_id]["log"].append({
            "step": iteration,
            "node": current,
            "state_snapshot": dict(state)
        })

        
        await run_tool(spec.nodes[current].fn, state)

        
        current = get_next_node(spec, current, state)

    RUNS[run_id]["status"] = "done"
    return run_id, RUNS[run_id]
