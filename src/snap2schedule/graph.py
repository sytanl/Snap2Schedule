import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .state import CalendarState
from .nodes import (
    extract_event_node,
    validate_event_node,
    clarification_node,
    check_conflict_node,
    conflict_warning_node,
    preview_event_node,
    create_event_node,
)
from .routing import (
    route_after_validation,
    route_after_conflict,
    route_after_conflict_warning,
    route_after_approval,
)


builder = StateGraph(CalendarState)


# Add nodes
builder.add_node("extract", extract_event_node)
builder.add_node("validate", validate_event_node)
builder.add_node("clarification", clarification_node)

builder.add_node("check_conflict", check_conflict_node)
builder.add_node("conflict_warning", conflict_warning_node)

builder.add_node("preview", preview_event_node)
builder.add_node("create", create_event_node)


# START -> extract
builder.add_edge(START, "extract")


# validate -> conditional routing
builder.add_conditional_edges(
    "validate",
    route_after_validation,
    {
        "complete": "check_conflict",
        "clarification": "clarification",
    },
)


# extract -> validate
builder.add_edge("extract", "validate")


# clarification -> extract again
builder.add_edge("clarification", "extract")


# check conflict -> conditional routing
builder.add_conditional_edges(
    "check_conflict",
    route_after_conflict,
    {
        "conflict": "conflict_warning",
        "no_conflict": "preview",
    },
)


# conflict warning -> conditional routing
builder.add_conditional_edges(
    "conflict_warning",
    route_after_conflict_warning,
    {
        "create_anyway": "preview",
        "cancel": END,
    },
)


# preview -> approval routing
builder.add_conditional_edges(
    "preview",
    route_after_approval,
    {
        "create": "create",
        "cancel": END,
    },
)


# create -> END
builder.add_edge("create", END)


# SQLite checkpointer
conn = sqlite3.connect(
    "checkpoints.sqlite",
    check_same_thread=False,
)

checkpointer = SqliteSaver(conn)


# Compile graph
graph = builder.compile(
    checkpointer=checkpointer,
)