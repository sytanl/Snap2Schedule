from datetime import datetime

def print_trace(
    node_name: str,
    state: dict,
):
    print("\n" + "=" * 50)
    print(f"[TRACE] Node: {node_name}")
    print(f"[TIME] {datetime.now().isoformat()}")

    if "user_input" in state:
        print(f"user_input: {state['user_input']}")

    if "extracted_event" in state:
        print(
            f"extracted_event: {state['extracted_event']}"
        )

    if "validation_result" in state:
        print(
            f"validation_result: {state['validation_result']}"
        )

    if "clarification_message" in state:
        print(
            f"clarification: {state['clarification_message']}"
        )

    print("=" * 50)