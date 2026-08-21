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
            errors.append("start_date cannot be after end_date")

    if extracted_event.start_time and extracted_event.end_time:
        if extracted_event.start_time < "00:00" or extracted_event.start_time > "24:00" or extracted_event.end_time < "00:00" or extracted_event.end_time > "24:00":
            errors.append("start_time and end_time must be valid times in 24-hour format (HH:MM)")
        if extracted_event.start_time > extracted_event.end_time:
            errors.append("end_datetime must be after start_datetime")
        if extracted_event.start_time == extracted_event.end_time and extracted_event.start_date == extracted_event.end_date:
            errors.append("end_datetime must be after start_datetim")

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
