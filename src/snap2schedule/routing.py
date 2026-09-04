from typing import Literal

from .state import CalendarState


def route_after_validation(
    state: CalendarState,
) -> Literal["complete", "clarification"]:

    if "validation_result" not in state:
        raise ValueError(
            "validation_result is required before routing"
        )

    validation_result = state["validation_result"]

    if validation_result.status == "valid":
        return "complete"

    return "clarification"  