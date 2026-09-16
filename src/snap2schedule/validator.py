from .schema import ExtractedEvent, ValidationResult

def validate_extracted_event(extracted_event: ExtractedEvent) -> ValidationResult:
    missing_fields = []
    errors = []

    # Check for required fields
    if not extracted_event.title:
        missing_fields.append("title")
    if not extracted_event.start_date:
        missing_fields.append("start_date")
    if not extracted_event.start_time:
        missing_fields.append("start_time")

    # Check for logical consistency
    if extracted_event.start_date and extracted_event.end_date:
        if extracted_event.start_date > extracted_event.end_date:
            errors.append("END_DATE_BEFORE_START_DATE")

    if extracted_event.start_time and extracted_event.end_time:
        if extracted_event.start_time < "00:00" or extracted_event.start_time > "24:00" or extracted_event.end_time < "00:00" or extracted_event.end_time > "24:00":
            errors.append("INVALID_TIME_FORMAT")
        if (extracted_event.start_time > extracted_event.end_time) or (extracted_event.start_time == extracted_event.end_time and extracted_event.start_date == extracted_event.end_date):
            errors.append("END_TIME_BEFORE_START_TIME")

    if missing_fields:
        status = "needs_clarification"
    elif errors:
        status = "invalid"
    else:
        status = "valid"

    return ValidationResult(
        status=status,
        errors=errors,
        missing_fields=missing_fields,
    )
