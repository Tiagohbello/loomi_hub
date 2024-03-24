from PIL import Image
import io
from django.core.files.base import ContentFile


def resize_image(image_field, max_size, quality):
    """
    Resizes an image to fit within a maximum size.

    Args:
    - image_field: The Django model ImageField containing the original image.
    - max_size: A tuple indicating the maximum width and height.
    - quality: The quality of the resulting image (1-100).

    Returns:
    A BytesIO object containing the resized image.
    """
    img = Image.open(image_field)
    img.thumbnail(max_size, Image.LANCZOS)

    temp_img = io.BytesIO()
    img.save(temp_img, "JPEG", quality=quality)
    temp_img.seek(0)
    return temp_img
