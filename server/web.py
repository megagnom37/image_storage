from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body, Query
from fastapi.responses import FileResponse
from typing import List, Optional
import asyncio
import shutil

from .models import Image
from .db_manager import PostgresDBManager
from .config import IST_IMAGE_STORAGE_FOLDER


app = FastAPI()
db_manager = PostgresDBManager()


@app.on_event("startup")
async def startup():
    await db_manager.init_db()


@app.get("/images", response_model=List[Image])
async def get_images_list():
    images_info = await db_manager.get_images()
    return images_info


@app.post("/add_image")
async def add_image(image: UploadFile = File(...),
                    image_tags: Optional[List[str]] = Form(None)):
    if image_tags:
        image_tags = list(set(image_tags[0].split(',')))
    else:
        image_tags = []

    image_info = Image(name=image.filename, tags=image_tags)

    image_path = f"{IST_IMAGE_STORAGE_FOLDER}/{image_info.id}_{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    await db_manager.store_image_info(image_info)

    return {'status': 'OK'}


@app.get("/get_image")
async def get_image(image_id: str):
    image_info = await db_manager.get_image(image_id)

    if not image_info:
        raise HTTPException(status_code=404, detail="Image not found")

    image_path = f"{IST_IMAGE_STORAGE_FOLDER}/{image_info.id}_{image_info.name}"

    return FileResponse(image_path, media_type="image/png")


@app.get("/images_by_tags", response_model=List[Image])
async def get_images_by_tags(tags: List[str] = Query(None)):
    images_info = await db_manager.get_images_by_tags(tags=tags)
    return images_info
