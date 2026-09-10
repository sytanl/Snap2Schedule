from typing import Literal

from .state import CalendarState


def route_after_validation(
    state: CalendarState,
) -> Literal["complete", "clarification"]:

    if "validation_result" not in state:
        raise ValueError(
            "validation_result is required before routing"
        )

    if state["validation_result"].status == "valid":
        route = "complete"
    else:
        route = "clarification"

    print(
        f"[ROUTE] validation -> {route}"
    )

    return route

def route_after_approval(
    state: CalendarState,
) -> Literal["create", "cancel"]:

    if state.get("approval") is True:
        return "create"

    return "cancel"

def route_after_conflict(
    state: CalendarState,
) -> Literal["conflict", "no_conflict"]:

    if state.get("conflict") is True:
        return "conflict"

    return "no_conflict"

def route_after_conflict_warning(
    state: CalendarState,
) -> Literal["create_anyway", "cancel"]:

    if state.get("create_anyway") is True:
        return "create_anyway"

    return "cancel"