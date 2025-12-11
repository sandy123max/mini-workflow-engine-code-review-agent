from typing import Callable, Dict, Any
import asyncio
import inspect

TOOL_REGISTRY: Dict[str, Callable] = {}

def register_tool(name: str):
    def decorator(fn: Callable):
        TOOL_REGISTRY[name] = fn
        return fn
    return decorator

async def run_tool(name: str, state: Dict[str, Any]):
    if name not in TOOL_REGISTRY:
        raise KeyError(f"Tool '{name}' is not registered")

    fn = TOOL_REGISTRY[name]

   
    if inspect.iscoroutinefunction(fn):
        return await fn(state)

 
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: fn(state))
