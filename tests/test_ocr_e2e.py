import sys
sys.path.append(".")

from src.snap2schedule.graph import graph


config = {
    "configurable": {
        "thread_id": "t28-test-01",
    }
}

result = graph.invoke(
    {
        "image_path": "tests/screenshots/test01.png",
        "user_input": "",
    },
    config=config,
)

print("Raw text:", result.get("raw_text"))
print("OCR confidence:", result.get("ocr_confidence"))
print("OCR engine:", result.get("ocr_engine"))
print("Extracted event:", result.get("extracted_event"))
print("Validation:", result.get("validation_result"))