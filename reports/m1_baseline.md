# M1 Baseline Report

Fixed context:
- Current datetime: 2026-08-20 10:00
- Timezone: Asia/Ho_Chi_Minh

Results:
- Total: 10
- Passed: 7
- Failed: 3
- Pass rate: 70%

Failures:
1. TC03 - RELATIVE_DATETIME_ERROR
   "next Monday" resolved to 2026-08-26 instead of 2026-08-24.

2. TC05 - TIME_DISAMBIGUATION_ERROR
   End time "9h xong" was interpreted as 09:00 instead of 21:00
   given the 19:00 event start.

3. TC08 - SCOPE_ERROR
   Reminder/task input was treated as a calendar event instead of
   being rejected as unsupported under V0.

Notes:
- TC06 validation correctly rejects end <= start, but clarification
  currently falls back to a generic invalid-input message because
  error-code mapping is not synchronized.