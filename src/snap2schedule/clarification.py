from .schema import ExtractedEvent, ValidationResult


def build_clarification(
    event: ExtractedEvent, 
    validation_result: ValidationResult,
) -> str | None:
    """
    Build a clarification message from an ExtractedEvent
    and its ValidationResult.
    """

    if validation_result.status == "valid":
        return None

    if validation_result.status == "needs_clarification":
        asked_fields: list[str] = []

        if "title" in validation_result.missing_fields:
            asked_fields.append("tiêu đề")

        if "start_date" in validation_result.missing_fields:
            asked_fields.append("ngày bắt đầu")

        if "start_time" in validation_result.missing_fields:
            asked_fields.append("thời gian bắt đầu")

        fields_text = ", ".join(asked_fields)

        return (
            f"Bạn có thể cung cấp {fields_text} "
            "cho sự kiện này không?"
        )

    if validation_result.status == "invalid":
        if "END_DATE_BEFORE_START_DATE" in validation_result.errors:
            return (
                "Ngày kết thúc không thể trước ngày bắt đầu. "
                "Bạn có thể cung cấp lại ngày bắt đầu và kết thúc không?"
            )

        if "INVALID_TIME_FORMAT" in validation_result.errors:
            return (
                "Thời gian phải đúng định dạng 24 giờ HH:MM "
                "(ví dụ 09:30 hoặc 14:00). "
                "Bạn vui lòng cung cấp lại nhé!"
            )

        if "INVALID_DATETIME_ORDER" in validation_result.errors:
            return (
                "Thời gian kết thúc phải sau thời gian bắt đầu. "
                "Bạn có thể cung cấp lại thông tin này không?"
            )

        return (
            "Thông tin đầu vào có vẻ không hợp lệ. "
            "Bạn hãy kiểm tra và cung cấp lại nhé!"
        )

    return None
