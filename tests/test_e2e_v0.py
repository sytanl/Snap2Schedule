from unittest.mock import patch
from langgraph.types import Command
import sys
sys.path.append(".")

from src.snap2schedule.graph import graph


def run_e2e(
    thread_id: str,
    user_input: str,
    responses: list[str],
    mock_conflict: bool = False,
):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    with patch(
        "src.snap2schedule.nodes.create_event",
        return_value="test-event-id",
    ), patch(
        "src.snap2schedule.nodes.get_events",
        return_value=[],
    ), patch(
        "src.snap2schedule.nodes.check_conflict",
        return_value=mock_conflict,
    ):
        result = graph.invoke(
            {
                "user_input": user_input,
            },
            config=config,
        )

        print("\nInitial result:")
        print(result)

        for response in responses:
            result = graph.invoke(
                Command(resume=response),
                config=config,
            )

            print(f"\nUser response: {response}")
            print(result)

        return result


# T01: Không conflict → approve → create
result = run_e2e(
    thread_id="e2e-v0-01",
    user_input=(
        "Ngày 15/9 lúc 14h họp team "
        "ở B201 khoảng 1 tiếng."
    ),
    responses=["có"],
)

assert result.get("approval") is True
assert result.get("event_id") is not None

print("\nT01 PASS")


# T02: Conflict → create anyway → approve → create
result = run_e2e(
    thread_id="e2e-v0-02",
    user_input=(
        "Ngày 10/9 lúc 14h họp team "
        "ở B201 khoảng 1 tiếng."
    ),
    responses=["có", "có"],
    mock_conflict=True,
)

assert result.get("conflict") is True
assert result.get("create_anyway") is True
assert result.get("approval") is True
assert result.get("event_id") is not None

print("\nT02 PASS")


# T03: Conflict → cancel
result = run_e2e(
    thread_id="e2e-v0-03",
    user_input=(
        "Ngày 10/9 lúc 14h họp team "
        "ở B201 khoảng 1 tiếng."
    ),
    responses=["không"],
    mock_conflict=True,
)

assert result.get("conflict") is True
assert result.get("create_anyway") is False
assert result.get("event_id") is None

print("\nT03 PASS")