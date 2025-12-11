from typing import Dict, Any, Optional
from pydantic import BaseModel

class NodeSpec(BaseModel):
    name: str
    fn: str
    condition_key: Optional[str] = None
    branches: Optional[Dict[str, str]] = None

class GraphSpec(BaseModel):
    graph_id: Optional[str] = None
    nodes: Dict[str, NodeSpec]
    edges: Dict[str, str]
    start_node: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
    max_iterations: int = 10
