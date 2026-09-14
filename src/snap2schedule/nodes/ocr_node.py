from ..state import CalendarState
from ..trace import print_trace
from ..paddleocr_tool import extract_text_from_image as paddleocr
from ..tesseract_tool import extract_text_from_image as tesseract

def ocr_input_node(
    state: CalendarState,
) -> dict:
    image_path = state["image_path"]
    result = {}

    try:
        raw_text, confidence = paddleocr(image_path)
        result["raw_text"] = raw_text
        result["user_input"] = raw_text
        result["ocr_confidence"] = confidence
        result["ocr_engine"] = "paddleocr"

        if confidence >= 0.85:
            print_trace(
                "ocr_input_node",
                {
                    **state,
                    **result,
                },
            )
            return result
    except Exception:
        pass

    try:
        raw_text, confidence = tesseract(image_path)
        result["raw_text"] = raw_text
        result["user_input"] = raw_text
        result["ocr_confidence"] = confidence
        result["ocr_engine"] = "tesseract"

        print_trace(
            "ocr_input_node",
            {
                **state,
                **result,
            },
        )
            
        return result
    except Exception as e:
        if "ocr_engine" in result:
            print_trace(
                "ocr_input_node",
                {
                    **state,
                    **result,
                },
            )
            return result
        else:
            from ..errors import OCRServiceError
            raise OCRServiceError(f"Both OCR engines failed. Last error: {e}")
