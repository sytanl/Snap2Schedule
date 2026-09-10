from datetime import date
from unittest.mock import patch

from langgraph.types import Command
import sys
sys.path.append(".")

from src.snap2schedule.schema import ExtractedEvent
from src.snap2schedule.graph import graph


def run_test(user_response: str):
    config = {
        "configurable": {
            "thread_id": f"test-approval-{user_response}"
        }
    }

    # Initial run → pause at approval
    result = graph.invoke(
        {
            "user_input": "Mai 2h chiều họp team ở B201 khoảng 1 tiếng."
        },
        config=config,
    )

    print("Initial:", result.get("__interrupt__"))

    # Resume with user's approval/rejection
    with patch(
        "src.snap2schedule.nodes.create_event",
        return_value="test-event-id",
    ) as mock_create:

        result = graph.invoke(
            Command(resume=user_response),
            config=config,
        )

        print("Response:", user_response)
        print("Approval:", result.get("approval"))
        print("Create called:", mock_create.called)

        return result, mock_create


# T01: User approves → create_event MUST be called
result, mock_create = run_test("có")

assert result["approval"] is True
assert mock_create.called

print("T01 PASS")


# T02: User rejects → create_event MUST NOT be called
result, mock_create = run_test("không")

assert result["approval"] is False
assert not mock_create.called

print("T02 PASS")