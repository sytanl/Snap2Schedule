import os

os.environ["FLAGS_enable_pir_api"] = "0"

from paddleocr import PaddleOCR


ocr = PaddleOCR(
    lang="vi",
    enable_mkldnn=False,
)

def extract_text_from_image(
    image_path: str,
) -> tuple[str, float]:

    result = ocr.predict(image_path)

    texts = []
    confidences = []

    for page in result:
        for text, confidence in zip(
            page["rec_texts"],
            page["rec_scores"],
        ):
            texts.append(text)
            confidences.append(float(confidence))

    raw_text = "\n".join(texts)

    confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    return raw_text, confidence