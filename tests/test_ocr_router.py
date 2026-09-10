from unittest.mock import patch
import sys
sys.path.append(".")

from src.snap2schedule.nodes import ocr_input_node


# T01: PaddleOCR confidence cao
with patch(
    "src.snap2schedule.nodes.paddleocr",
    return_value=("Mai 2h họp team", 0.95),
):
    result = ocr_input_node("test.png")

    print("T01:", result)

    assert result["ocr_engine"] == "paddleocr"
    assert result["ocr_confidence"] == 0.95


# T02: PaddleOCR confidence thấp → fallback Tesseract
with patch(
    "src.snap2schedule.nodes.paddleocr",
    return_value=("Mai 2h hop team", 0.70),
), patch(
    "src.snap2schedule.nodes.tesseract",
    return_value=("Mai 2h họp team", 0.88),
):
    result = ocr_input_node("test.png")

    print("T02:", result)

    assert result["ocr_engine"] == "tesseract"
    assert result["ocr_confidence"] == 0.88


print("All T27 tests PASS")