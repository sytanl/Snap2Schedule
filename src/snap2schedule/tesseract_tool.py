import pytesseract
from PIL import Image


def extract_text_from_image(
    image_path: str,
) -> tuple[str, float]:

    image = Image.open(image_path)

    data = pytesseract.image_to_data(
        image,
        lang="eng",
        output_type=pytesseract.Output.DICT,
    )

    texts = []
    confidences = []

    for text, confidence in zip(
        data["text"],
        data["conf"],
    ):
        text = text.strip()

        if not text:
            continue

        confidence = float(confidence)

        if confidence >= 0:
            texts.append(text)
            confidences.append(confidence / 100.0)

    raw_text = " ".join(texts)

    confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    return raw_text, confidence