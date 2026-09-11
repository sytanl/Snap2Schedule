from unittest.mock import Mock
import sys
sys.path.append(".")

from src.snap2schedule.retry import retry


def main() -> None:
    # T01 - success immediately
    mock = Mock(return_value="OK")

    result = retry(mock, max_retries=1)

    assert result == "OK"
    assert mock.call_count == 1

    print("T01 PASS - success without retry")

    # T02 - fail once, then success
    mock = Mock(
        side_effect=[
            RuntimeError("temporary error"),
            "OK",
        ]
    )

    result = retry(mock, max_retries=1)

    assert result == "OK"
    assert mock.call_count == 2

    print("T02 PASS - one bounded retry")

    # T03 - fail twice
    mock = Mock(
        side_effect=[
            RuntimeError("error 1"),
            RuntimeError("error 2"),
        ]
    )

    try:
        retry(mock, max_retries=1)
    except RuntimeError:
        pass
    else:
        raise AssertionError(
            "Expected RuntimeError was not raised"
        )

    assert mock.call_count == 2

    print("T03 PASS - stops after max retry")

    # T04 - persistent failure must not retry forever
    mock = Mock(
        side_effect=RuntimeError("persistent error")
    )

    try:
        retry(mock, max_retries=1)
    except RuntimeError:
        pass

    assert mock.call_count == 2

    print("T04 PASS - no infinite retry")

    print()
    print("T30: 4/4 PASS")


if __name__ == "__main__":
    main()
