from src.snap2schedule.graph import graph
from langgraph.types import Command

config = {
    "configurable": {
        "thread_id": "test-001"
    }
}

result = graph.invoke(
    {
        "user_input": "Chiều mai họp với Minh nhé."
    },
    config=config,
)

print(result)

result = graph.invoke(
    Command(resume="2h, 1 tiếng"),
    config=config,
)

print(result)