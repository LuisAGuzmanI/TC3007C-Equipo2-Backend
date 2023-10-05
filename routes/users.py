from fastapi import APIRouter, UploadFile, File

from models.users import User
from config.database import users
from schema.schemas import list_serial
from bson import ObjectId

from helpers.video_to_images import video_to_face_images
from helpers.main_recognition import recognition_manager

router = APIRouter()

@router.post("/upload-profile-picture/{id}")
async def upload_profile_picture(id: str, file: UploadFile = File(...)):
    return  await print(video_to_face_images('users', id, file))

@router.post("/facial-recognition/{id}")
async def post_user_dataset(id: str, file: UploadFile = File(...)):
    return await recognition_manager('users', id)
    # return list_serial(users.find())

# Get
@router.get("/")
async def get_users():
    return list_serial(users.find())

# Post
@router.post("/")
async def post_user(user: User):
    users.insert_one(dict(user))

# Put
@router.put("/{id}")
async def put_user(id: str, user: User):
    users.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

# Delete
@router.delete("/{id}")
async def delete_user(id: str):
    users.find_one_and_delete({"_id": ObjectId(id)})

    