import os
import logging

from fastapi import Depends, HTTPException, UploadFile, File, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session

import model
from database import get_db
from utils import greyscale_image


UPLOADED_FILE = "uploaded_files"
os.makedirs(UPLOADED_FILE, exist_ok=True)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_files(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOADED_FILE, file.filename)
    file_content = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    newfile = model.Picture(filename=file.filename, picture=file_content)
    db.add(newfile)
    db.commit()

    return {"filename": file.filename}


@router.get("/download/")
async def download_file(db: Session = Depends(get_db)):
    try:
        file = db.query(model.Picture).order_by(desc(model.Picture.id)).first()

        if file is None or not file.picture:
            raise HTTPException(status_code=404, detail="No picture found")

        file_path, media_type = greyscale_image(file)

        return StreamingResponse(open(file_path, "rb"), media_type=media_type)
    except Exception as e:
        logger.error("Error downloading file: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
