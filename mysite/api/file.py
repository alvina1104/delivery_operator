import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from mysite.api.auth import get_current_user
from mysite.database.db import SessionLocal
from mysite.database.models import FileObject, UserProfile
from mysite.database.schema import FileObjectOutSchema


file_router = APIRouter(prefix="/file", tags=["File"])

os.makedirs("media", exist_ok=True)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@file_router.post("/", response_model=FileObjectOutSchema)
async def create_file(dataset_file: UploadFile, task_file: UploadFile | None = None, img_file: UploadFile | None = None, db: Session = Depends(get_db), current_user: UserProfile = Depends(get_current_user)):
    dataset_path = os.path.join("media", os.path.basename(dataset_file.filename))
    with open(dataset_path, "wb") as f:
        f.write(await dataset_file.read())

    task_path = None
    if task_file and task_file.filename:
        task_path = os.path.join("media", os.path.basename(task_file.filename))
        with open(task_path, "wb") as f:
            f.write(await task_file.read())

    img_path = None
    if img_file and img_file.filename:
        img_path = os.path.join("media", os.path.basename(img_file.filename))
        with open(img_path, "wb") as f:
            f.write(await img_file.read())

    file_data = FileObject(
        dataset_file=dataset_path,
        task_file=task_path,
        img_file=img_path,
        user_id=current_user.id
    )

    db.add(file_data)
    db.commit()
    db.refresh(file_data)

    return file_data

@file_router.get("/", response_model=List[FileObjectOutSchema])
async def list_file(db: Session = Depends(get_db), current_user: UserProfile = Depends(get_current_user)):
    return db.query(FileObject).filter(FileObject.user_id == current_user.id).all()


@file_router.delete("/{file_id}/", response_model=dict)
async def delete_file(file_id: int, db: Session = Depends(get_db), current_user: UserProfile = Depends(get_current_user)):
    file_db = db.query(FileObject).filter(FileObject.id == file_id,FileObject.user_id == current_user.id).first()

    if not file_db:
        raise HTTPException(status_code=404, detail="Такого файла нету")

    db.delete(file_db)
    db.commit()

    return {"message": "File успешно удалено"}