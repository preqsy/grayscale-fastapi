import io
import mimetypes
import os
import cv2
from fastapi import HTTPException
import numpy as np
import pyheif
from PIL import Image

UPLOADED_FILE = "uploaded_files"
os.makedirs(UPLOADED_FILE, exist_ok=True)


def greyscale_image(file):
    image_data = io.BytesIO(file.picture)

    img = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=500, detail="Failed to load image")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(
        UPLOADED_FILE, f"gray_{os.path.splitext(file.filename)[0]}{file_extension}"
    )
    cv2.imwrite(file_path, gray_img)
    mime_type, _ = mimetypes.guess_type(file_path)
    media_type = mime_type if mime_type else "application/octet-stream"
    if mime_type == "image/heic":
        heif_image = pyheif.read(image_data)
        image = Image.frombytes(
            heif_image.mode,
            heif_image.size,
            heif_image.data,
            "raw",
            heif_image.mode,
            heif_image.stride,
        )
        jpeg_path = file_path.replace(".heic", ".jpeg")
        image.save(jpeg_path, "JPEG")
        file_path = jpeg_path
    return file_path, media_type
