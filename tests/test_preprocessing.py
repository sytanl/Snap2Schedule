from pathlib import Path

from PIL import Image
import sys
sys.path.append(".")

from src.snap2schedule.image_preprocess import (
    grayscale,
    upscale,
    threshold,
)
from src.snap2schedule.paddleocr_tool import extract_text_from_image


image_paths = list(
    Path("tests/screenshots").glob("*.png")
)


for image_path in image_paths:
    print("=" * 60)
    print("Image:", image_path)

    # Before
    raw_text, confidence = extract_text_from_image(
        str(image_path)
    )

    print("BEFORE")
    print("Text:", raw_text)
    print("Confidence:", confidence)

    image = Image.open(image_path)

    techniques = {
        "grayscale": grayscale(image),
        "upscale": upscale(image),
        "threshold": threshold(image),
    }

    for name, processed_image in techniques.items():
        output_path = Path(
            "tests/screenshots"
        ) / f"{image_path.stem}_{name}.png"

        processed_image.save(output_path)

        raw_text, confidence = extract_text_from_image(
            str(output_path)
        )

        print(f"\nAFTER - {name}")
        print("Text:", raw_text)
        print("Confidence:", confidence)