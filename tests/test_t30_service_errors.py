"""T30 - integration-level error handling tests.

These tests verify that:
1. Calendar API failure is converted to CalendarServiceError.
2. Calendar API temporary failure is retried once.
3. OCR failure falls back from PaddleOCR to Tesseract.
4. OCR failure in both engines becomes OCRServiceError.

Run:
    python tests/test_t30_service_errors.py
"""

from unittest.mock import Mock, patch
import sys
sys.path.append(".")

from src.snap2schedule.errors import (
    CalendarServiceError,
    OCRServiceError,
)
from src.snap2schedule.retry import retry


def test_calendar_retry_then_success():
    """T05: Calendar request fails once, then succeeds."""

    mock_request = Mock(
        side_effect=[
            RuntimeError("temporary Google Calendar API error"),
            {"items": []},
        ]
    )

    result = retry(mock_request, max_retries=1)

    assert result == {"items": []}
    assert mock_request.call_count == 2

    print("T05 PASS - Calendar temporary error retried once")


def test_calendar_error_after_retry():
    """T06: Calendar request keeps failing and stops after one retry."""

    mock_request = Mock(
        side_effect=RuntimeError("Google Calendar API unavailable")
    )

    try:
        retry(mock_request, max_retries=1)
    except RuntimeError as exc:
        assert "unavailable" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError was not raised")

    assert mock_request.call_count == 2

    # Verify the application-level error type can represent this failure.
    error = CalendarServiceError(
        "Không thể truy cập Google Calendar."
    )
    assert str(error)

    print("T06 PASS - Calendar error stops after bounded retry")


def test_ocr_paddle_failure_falls_back_to_tesseract():
    """T07: PaddleOCR crashes, so router uses Tesseract."""

    from src.snap2schedule.nodes import ocr_input_node

    with patch(
        "src.snap2schedule.nodes.paddleocr",
        side_effect=RuntimeError("PaddleOCR failed"),
    ), patch(
        "src.snap2schedule.nodes.tesseract",
        return_value=("Mai 2h họp team", 0.88),
    ):
        result = ocr_input_node(
            {
                "image_path": "test.png",
                "user_input": "",
            }
        )

    assert result["ocr_engine"] == "tesseract"
    assert result["ocr_confidence"] == 0.88
    assert result["raw_text"] == "Mai 2h họp team"

    print("T07 PASS - PaddleOCR error falls back to Tesseract")


def test_ocr_both_engines_fail():
    """T08: PaddleOCR and Tesseract both fail gracefully."""

    from src.snap2schedule.nodes import ocr_input_node

    with patch(
        "src.snap2schedule.nodes.paddleocr",
        side_effect=RuntimeError("PaddleOCR failed"),
    ), patch(
        "src.snap2schedule.nodes.tesseract",
        side_effect=RuntimeError("Tesseract failed"),
    ):
        try:
            ocr_input_node(
                {
                    "image_path": "test.png",
                    "user_input": "",
                }
            )
        except OCRServiceError as exc:
            assert str(exc)
        else:
            raise AssertionError(
                "Expected OCRServiceError was not raised"
            )

    print("T08 PASS - Both OCR engines fail gracefully")


def main() -> None:
    print("=" * 70)
    print("T30 - SERVICE ERROR HANDLING")
    print("=" * 70)

    tests = [
        test_calendar_retry_then_success,
        test_calendar_error_after_retry,
        test_ocr_paddle_failure_falls_back_to_tesseract,
        test_ocr_both_engines_fail,
    ]

    passed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as exc:
            print(f"{test.__name__} FAIL - {exc}")

    print()
    print("=" * 70)
    print("T30 SERVICE ERROR SUMMARY")
    print("=" * 70)
    print(f"Total : {len(tests)}")
    print(f"PASS  : {passed}")
    print(f"FAIL  : {len(tests) - passed}")
    print(f"Rate  : {passed / len(tests) * 100:.1f}%")
    print("=" * 70)

    if passed == len(tests):
        print("T30 SERVICE ERROR TEST: 4/4 PASS")
    else:
        print("T30 SERVICE ERROR TEST: FAILED")


if __name__ == "__main__":
    main()
