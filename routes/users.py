from fastapi import APIRouter, UploadFile, File

from models.users import User, Student
from config.database import users
from schema.schemas import list_serial, individual_serial
from bson import ObjectId, is_valid

from helpers.video_to_images import video_to_face_images
from helpers.main_recognition import recognition_manager

from typing import List

router = APIRouter()

@router.post("/upload-profile-picture/{id}")
async def upload_profile_picture(id: str, file: UploadFile = File(...)):
    result = await video_to_face_images('users', id, file)
    print(result)
    return result

@router.post("/facial-recognition/{id}/{name}")
async def post_user_dataset(id: str, name: str, file: UploadFile = File(...)):
    return await recognition_manager('users', id, name, file)
    # return list_serial(users.find())

@router.get("/by-id/{id}")
async def get_user_by_id(id: str):
    return individual_serial(users.find_one({'user_id': id}))

# Get
@router.get("/by-id/{id}")
async def get_users_by_id(id: str):
    return individual_serial(users.find_one({'user_id': id}))

@router.get("/get-students")
async def get_students():
    return list_serial(users.find({'role': 'student'}))

# Post
@router.post("/create-user")
async def post_user(user: User):
    users.insert_one(dict(user))

@router.post("/create-students")
async def post_user(students: List[Student]):
    for student in students:
        print(student)
        users.insert_one(dict(student))

# Put
@router.put("/{id}")
async def put_user(id: str, user: User):
    users.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

# Delete
@router.delete("/{id}")
async def delete_user(id: str):
    users.find_one_and_delete({"_id": ObjectId(id)})

    