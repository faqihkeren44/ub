import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException
from supabase import create_client

from app.core.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    SUPABASE_BUCKET
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}

MAX_FILE_SIZE = 2 * 1024 * 1024

def validate_extension(filename: str):

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Format gambar harus JPG, JPEG, atau PNG."
        )

    return extension

async def validate_size(file: UploadFile):

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Ukuran maksimal 2 MB."
        )

    await file.seek(0)

def generate_filename(extension):

    return f"{uuid.uuid4()}{extension}"

async def upload_image(file: UploadFile, BUCKET_NAME):

    extension = validate_extension(file.filename)

    await validate_size(file)

    filename = generate_filename(extension)

    data = await file.read()

    path = f"member/{filename}"

    response = (
        supabase
        .storage
        .from_(BUCKET_NAME)
        .upload(
            path,
            data,
            {
                "content-type": file.content_type
            }
        )
    )

    return path

def get_public_url(path, BUCKET_NAME):

    return (
        supabase
        .storage
        .from_(BUCKET_NAME)
        .get_public_url(path)
    )

def delete_image(path):

    if not path:
        return

    (
        supabase
        .storage
        .from_(SUPABASE_BUCKET)
        .remove([path])
    )