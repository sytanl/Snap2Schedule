class Snap2ScheduleError(Exception):
    """Base application error."""


class OCRServiceError(Snap2ScheduleError):
    """OCR processing failed."""


class CalendarServiceError(Snap2ScheduleError):
    """Google Calendar API failed."""


class CalendarTimeoutError(CalendarServiceError):
    """Google Calendar request timed out."""
