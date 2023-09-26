from fastapi import APIRouter

from models.users import User
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# Get
@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos
# Post
@router.post("/")
async def post_todo(user: User):
    collection_name.insert_one(dict(user))

# Put
@router.put("/{id}")
async def put_todo(id: str, user: User):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

# Delete
@router.delete("/{id}")
async def put_todo(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})

    