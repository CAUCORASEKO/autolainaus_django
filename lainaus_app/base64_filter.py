from django import template
import base64
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

register = template.Library()

@register.filter
def base64_image(value):
    """
    Convierte una imagen en un string codificado en base64.
    """
    try:
        image = Image.open(value)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        return f"Error: {str(e)}"
