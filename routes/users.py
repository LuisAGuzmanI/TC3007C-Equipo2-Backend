from fastapi import APIRouter

from models.users import User
from config.database import users
from schema.schemas import list_serial
from bson import ObjectId


router = APIRouter()

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

    