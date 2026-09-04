# from langgraph.checkpoint.memory import InMemorySaver
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .state import CalendarState
from .nodes import (
    extract_event_node,
    validate_event_node,
    clarification_node,
)
from .routing import route_after_validation

builder = StateGraph(CalendarState)

# add nodes
builder.add_node("extract", extract_event_node)
builder.add_node("validate", validate_event_node)
builder.add_node("clarification", clarification_node)

# START -> extract
builder.add_edge(START, "extract")

# extract -> validate
builder.add_edge("extract", "validate")

# validate -> conditional routing
builder.add_conditional_edges(
    "validate",
    route_after_validation,
    {
        "complete": END,
        "clarification": "clarification",
    },
)

# clarification -> extract again
builder.add_edge("clarification", "extract")

conn = sqlite3.connect(
    "checkpoints.sqlite",
    check_same_thread=False,
)

checkpointer = SqliteSaver(conn)

graph = builder.compile(
    checkpointer=checkpointer
)   