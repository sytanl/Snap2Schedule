import sys
sys.path.append(".")

from datetime import datetime
from zoneinfo import ZoneInfo
from src.snap2schedule.time_context import TimeContext
from src.snap2schedule.extractor import extract_event
from src.snap2schedule.validator import validate_extracted_event
from src.snap2schedule.clarification import build_clarification

fixed = datetime(
    2026,
    8,
    20,
    10,
    0,
    tzinfo=ZoneInfo("Asia/Ho_Chi_Minh"),
)

ctx = TimeContext(fixed_datetime=fixed)

TC01 = "Mai 2h chiều họp team ở B201 khoảng 1 tiếng, review OCR sprint."
TC02 = "Thứ 6 tuần này 9h review sprint với team AI."
TC03 = "Meeting with John next Monday at 2 PM for 45 minutes in A302."
TC04 = "Chiều mai họp với Minh nhé."
TC05 = "Ngày 22/8 lúc 7h tối đi workshop AI Engineer Meetup ở Dreamplex, 9h xong."
TC06 = "Mai 14h họp, kết thúc 13h30."
TC07 = "Let's sync sometime tomorrow afternoon."
TC08 = "Nhắc tôi mua sữa mai."
TC09 = "Họp project OCR lúc 14:30 ngày 20/8/2026."
TC10 = "Ngày mai 8h30 review demo LangGraph, tầm 1 tiếng."


for i, test_case in enumerate([TC01, TC02, TC03, TC04, TC05, TC06, TC07, TC08, TC09, TC10]):
    extracted = extract_event(test_case, time_context=ctx)
    validation = validate_extracted_event(extracted)
    clarification = build_clarification(extracted, validation)
    
    print(f"TEST CASE {i+1}: {test_case}")
    print("Extracted: ", extracted)
    print("Validation: ", validation)
    print("Clarification: ", clarification)
    print("\n")