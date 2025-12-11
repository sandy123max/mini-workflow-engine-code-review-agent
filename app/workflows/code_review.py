import re
import statistics
from typing import Dict, Any
from app.registry import register_tool

@register_tool("extract_functions")
def extract_functions(state: Dict[str, Any]):
    code = state.get("code", "")
    parts = re.split(r'(?m)^(?=def )', code)

    functions = []
    for part in parts:
        match = re.match(r'def\s+(\w+)\(', part)
        if match:
            name = match.group(1)
            lines = part.strip().splitlines()
            complexity = sum(1 for l in lines if re.search(r'\b(if|for|while|elif|try|except)\b', l))
            functions.append({
                "name": name,
                "lines": len(lines),
                "complexity": complexity
            })

    state["functions"] = functions
    return {"functions": functions}

@register_tool("check_complexity")
def check_complexity(state: Dict[str, Any]):
    funcs = state.get("functions", [])

    for f in funcs:
        f["complexity_score"] = f["lines"] * 0.6 + f["complexity"] * 2

    avg = statistics.mean([f["complexity_score"] for f in funcs]) if funcs else 0
    state["complexity_score"] = avg

    return {"complexity_score": avg}

@register_tool("detect_issues")
def detect_issues(state: Dict[str, Any]):
    funcs = state.get("functions", [])
    issues = []

    for f in funcs:
        if f["lines"] > 50:
            issues.append({"fn": f["name"], "issue": "long_function"})
        if f["complexity_score"] > 40:
            issues.append({"fn": f["name"], "issue": "high_complexity"})
        if "TODO" in f.get("text", ""):
            issues.append({"fn": f["name"], "issue": "todo_comment"})

    state["issues"] = issues
    state["issues_count"] = len(issues)

    return {"issues": issues, "issues_count": len(issues)}

@register_tool("suggest_improvements")
def suggest_improvements(state: Dict[str, Any]):
    issues = state.get("issues", [])
    suggestions = []

    for issue in issues:
        suggestions.append({"fix": f"Resolved {issue['issue']} in {issue['fn']}"})

    score = 100 - (state.get("complexity_score", 0) + len(issues) * 5)
    state["quality_score"] = max(score, 0)

    return {"quality_score": state["quality_score"], "suggestions": suggestions}
