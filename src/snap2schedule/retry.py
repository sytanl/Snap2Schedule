from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


def retry(
    func: Callable[[], T],
    max_retries: int = 1,
) -> T:
    """Run func and retry at most max_retries times."""
    last_error: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as exc:
            last_error = exc

            if attempt >= max_retries:
                raise

    # Defensive fallback; normally unreachable.
    assert last_error is not None
    raise last_error
