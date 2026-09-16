from unittest.mock import patch

from langgraph.types import Command
import sys
sys.path.append(".")

from src.snap2schedule.graph import graph


def run_test(
    thread_id: str,
    approval_responses: list[str],
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
    ) as mock_create, patch(
        "src.snap2schedule.nodes.get_events",
        return_value=[],
    ), patch(
        "src.snap2schedule.nodes.check_conflict",
        return_value=mock_conflict,
    ):

        result = graph.invoke(
            {
                "user_input": (
                    "Ngày 10/9 lúc 14h họp team "
                    "ở B201 khoảng 1 tiếng."
                )
            },
            config=config,
        )

        print("Initial interrupt:", result.get("__interrupt__"))

        for response in approval_responses:
            result = graph.invoke(
                Command(resume=response),
                config=config,
            )

            print("Response:", response)
            print("State:", result)
            print("Create called:", mock_create.called)

        return result, mock_create


# T01: No conflict → preview → approve → create
result, mock_create = run_test(
    "t22-no-conflict",
    ["có"],
)

assert mock_create.called

print("T01 PASS")


# T02: Have conflict → warning → create anyway → preview → approve → create
result, mock_create = run_test(
    "t22-conflict-create",
    ["có", "có"],
    mock_conflict=True,
)

assert mock_create.called

print("T02 PASS")


# T03: Have conflict → warning → cancel
result, mock_create = run_test(
    "t22-conflict-cancel",
    ["không"],
    mock_conflict=True,
)

assert not mock_create.called

print("T03 PASS")