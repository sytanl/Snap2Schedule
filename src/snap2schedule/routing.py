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