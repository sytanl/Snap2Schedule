import sys
sys.path.append(".")

from src.snap2schedule.tesseract_tool import extract_text_from_image


image_paths = [
    "tests/screenshots/test01.png",
    "tests/screenshots/test02.png",
    "tests/screenshots/test03.png",
    "tests/screenshots/test04.png",
    "tests/screenshots/test05.png",
]


for image_path in image_paths:
    raw_text, confidence = extract_text_from_image(image_path)

    print("=" * 50)
    print("Image:", image_path)
    print("Raw text:", raw_text)
    print("Confidence:", confidence)