from datetime import datetime
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.append(".")

from src.snap2schedule.extractor import extract_event
from src.snap2schedule.validator import validate_extracted_event
from src.snap2schedule.calendar.conflict_checker import check_conflict
from src.snap2schedule.schema import CalendarEventSummary
from src.snap2schedule.nodes import ocr_input_node


# ============================================================
# TEST CASES
# ============================================================

results = []


def record(case_id: str, description: str, passed: bool, detail: str = ""):
    results.append(
        {
            "id": case_id,
            "description": description,
            "passed": passed,
            "detail": detail,
        }
    )

    status = "PASS" if passed else "FAIL"
    msg = f"{case_id}: {status} - {description}"
    print(msg.encode('utf-8').decode('cp1252', 'ignore'))

    if detail:
        print(f"      {detail}")


def run_extraction_case(
    case_id: str,
    text: str,
    expected_status: str,
    expected_start_time: str | None = None,
    expected_end_time: str | None = None,
):
    try:
        event = extract_event(text)
        validation = validate_extracted_event(event)

        passed = validation.status == expected_status

        if expected_start_time is not None:
            passed = passed and event.start_time == expected_start_time

        if expected_end_time is not None:
            passed = passed and event.end_time == expected_end_time

        record(
            case_id,
            text,
            passed,
            (
                f"status={validation.status}, "
                f"start={event.start_time}, "
                f"end={event.end_time}"
            ),
        )

    except Exception as exc:
        record(
            case_id,
            text,
            False,
            f"Exception: {exc}",
        )


# ============================================================
# 1. TEXT + VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("GROUP 1 - TEXT EXTRACTION + VALIDATION")
print("=" * 70)

run_extraction_case(
    "T01",
    "Mai 2h chiều họp team ở B201 khoảng 1 tiếng.",
    "valid",
    "14:00",
    "15:00",
)

run_extraction_case(
    "T02",
    "Thứ 6 tuần này 9h review sprint với team AI.",
    "valid",
    "09:00",
)

run_extraction_case(
    "T03",
    "Meeting with John next Monday at 2 PM for 45 minutes in A302.",
    "valid",
    "14:00",
    "14:45",
)

run_extraction_case(
    "T04",
    "Chiều mai họp với Minh nhé.",
    "needs_clarification",
)

run_extraction_case(
    "T05",
    "Nhắc tôi mua sữa mai.",
    "needs_clarification",
)

run_extraction_case(
    "T06",
    "Mai 14h họp team, kết thúc 13h30.",
    "invalid",
)

run_extraction_case(
    "T07",
    "Họp project OCR lúc 14:30 ngày 20/8/2026.",
    "valid",
    "14:30",
)

run_extraction_case(
    "T08",
    "Ngày mai 8h30 review demo LangGraph, tầm 1 tiếng.",
    "valid",
    "08:30",
    "09:30",
)

run_extraction_case(
    "T09",
    "Let's sync sometime tomorrow afternoon.",
    "needs_clarification",
)

run_extraction_case(
    "T10",
    "Ngày 22/8 lúc 7h tối đi workshop AI Engineer Meetup ở Dreamplex, 9h xong.",
    "valid",
)


# ============================================================
# 2. OCR E2E
# ============================================================

print("\n" + "=" * 70)
print("GROUP 2 - SCREENSHOT OCR")
print("=" * 70)

SCREENSHOT_DIR = Path("tests/screenshots")

ocr_cases = [
    ("T11", "test01.png"),
    ("T12", "test02.png"),
    ("T13", "test03.png"),
    ("T14", "test04.png"),
    ("T15", "test05.png"),
]


for case_id, filename in ocr_cases:
    image_path = SCREENSHOT_DIR / filename

    try:
        if not image_path.exists():
            record(
                case_id,
                f"OCR {filename}",
                False,
                "Screenshot not found",
            )
            continue

        state = {
            "image_path": str(image_path),
            "user_input": "",
        }

        ocr_result = ocr_input_node(state)

        raw_text = ocr_result.get("raw_text")
        confidence = ocr_result.get("ocr_confidence")
        engine = ocr_result.get("ocr_engine")

        passed = (
            isinstance(raw_text, str)
            and len(raw_text.strip()) > 0
            and isinstance(confidence, float)
            and 0.0 <= confidence <= 1.0
            and engine in {"paddleocr", "tesseract"}
        )

        record(
            case_id,
            f"OCR {filename}",
            passed,
            (
                f"engine={engine}, "
                f"confidence={confidence:.3f}, "
                f"text={raw_text}"
            ),
        )

    except Exception as exc:
        record(
            case_id,
            f"OCR {filename}",
            False,
            f"Exception: {exc}",
        )


# ============================================================
# 3. OCR ROUTER
# ============================================================

print("\n" + "=" * 70)
print("GROUP 3 - OCR ROUTER / FALLBACK")
print("=" * 70)


# T16: Paddle confidence cao -> PaddleOCR
try:
    with patch(
        "src.snap2schedule.nodes.paddleocr",
        return_value=("Mai 2h họp team", 0.95),
    ):
        result = ocr_input_node(
            {
                "image_path": "test.png",
                "user_input": "",
            }
        )

    passed = (
        result["ocr_engine"] == "paddleocr"
        and result["ocr_confidence"] == 0.95
    )

    record(
        "T16",
        "High confidence -> PaddleOCR",
        passed,
        str(result),
    )

except Exception as exc:
    record(
        "T16",
        "High confidence -> PaddleOCR",
        False,
        f"Exception: {exc}",
    )


# T17: Paddle confidence thấp -> Tesseract
try:
    with patch(
        "src.snap2schedule.nodes.paddleocr",
        return_value=("Mai 2h hop team", 0.70),
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

    passed = (
        result["ocr_engine"] == "tesseract"
        and result["ocr_confidence"] == 0.88
    )

    record(
        "T17",
        "Low confidence -> Tesseract fallback",
        passed,
        str(result),
    )

except Exception as exc:
    record(
        "T17",
        "Low confidence -> Tesseract fallback",
        False,
        f"Exception: {exc}",
    )


# ============================================================
# 4. CONFLICT CHECKER
# ============================================================

print("\n" + "=" * 70)
print("GROUP 4 - CONFLICT CHECKING")
print("=" * 70)


existing_events = [
    CalendarEventSummary(
        id="event-001",
        title="Existing meeting",
        start="2026-09-10T14:00:00+07:00",
        end="2026-09-10T15:00:00+07:00",
    )
]


# T18: overlapping -> conflict
try:
    conflict = check_conflict(
        datetime.fromisoformat(
            "2026-09-10T14:30:00+07:00"
        ),
        datetime.fromisoformat(
            "2026-09-10T15:30:00+07:00"
        ),
        existing_events,
    )

    record(
        "T18",
        "Overlapping event -> conflict",
        conflict is True,
        f"conflict={conflict}",
    )

except Exception as exc:
    record(
        "T18",
        "Overlapping event -> conflict",
        False,
        f"Exception: {exc}",
    )


# T19: non-overlapping -> no conflict
try:
    conflict = check_conflict(
        datetime.fromisoformat(
            "2026-09-10T15:00:00+07:00"
        ),
        datetime.fromisoformat(
            "2026-09-10T16:00:00+07:00"
        ),
        existing_events,
    )

    record(
        "T19",
        "Non-overlapping event -> no conflict",
        conflict is False,
        f"conflict={conflict}",
    )

except Exception as exc:
    record(
        "T19",
        "Non-overlapping event -> no conflict",
        False,
        f"Exception: {exc}",
    )


# T20: boundary case
try:
    conflict = check_conflict(
        datetime.fromisoformat(
            "2026-09-10T13:00:00+07:00"
        ),
        datetime.fromisoformat(
            "2026-09-10T14:00:00+07:00"
        ),
        existing_events,
    )

    record(
        "T20",
        "Event ending exactly at existing start -> no conflict",
        conflict is False,
        f"conflict={conflict}",
    )

except Exception as exc:
    record(
        "T20",
        "Event ending exactly at existing start -> no conflict",
        False,
        f"Exception: {exc}",
    )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("T29 REGRESSION TEST SUMMARY")
print("=" * 70)

total = len(results)
passed = sum(1 for result in results if result["passed"])
failed = total - passed

print(f"Total : {total}")
print(f"PASS  : {passed}")
print(f"FAIL  : {failed}")

if total > 0:
    pass_rate = passed / total * 100
    print(f"Rate  : {pass_rate:.1f}%")

print("=" * 70)

if failed == 0:
    print("T29 RESULT: 20/20 PASS")
    print("V1 regression suite PASSED.")
else:
    print(f"T29 RESULT: {passed}/{total} PASS")
    print("V1 regression suite has failures.")

    print("\nFailed cases:")
    for result in results:
        if not result["passed"]:
            print(
                f"- {result['id']}: "
                f"{result['description']}"
            )