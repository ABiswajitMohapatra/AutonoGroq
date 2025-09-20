from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, add_messages

class GraphState(TypedDict):
    facts: Annotated[list, add_messages]

graph = StateGraph(GraphState)

def add_fact(subject, relation, obj):
    current_facts = getattr(graph, "facts", [])
    current_facts.append((subject, relation, obj))
    graph.facts = current_facts

def query_fact(subject=None, relation=None):
    results = getattr(graph, "facts", [])
    if subject and relation:
        return [f for f in results if f[0] == subject and f[1] == relation]
    elif subject:
        return [f for f in results if f[0] == subject]
    else:
        return results
