from PIL import Image, ImageOps


def grayscale(image: Image.Image) -> Image.Image:
    return ImageOps.grayscale(image)


def upscale(
    image: Image.Image,
    scale: int = 2,
) -> Image.Image:
    return image.resize(
        (image.width * scale, image.height * scale)
    )


def threshold(
    image: Image.Image,
    value: int = 180,
) -> Image.Image:
    gray = ImageOps.grayscale(image)

    return gray.point(
        lambda pixel: 255 if pixel > value else 0
    )