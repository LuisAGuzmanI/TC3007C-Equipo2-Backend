from fastapi import APIRouter

from models.classrooms import Classroom
from config.database import classrooms
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# Get
@router.get("/")
async def get_classrooms():
    return list_serial(classrooms.find())

# Post
@router.post("/")
async def post_classroom(classroom: Classroom):
    c = dict(classroom)
    c["professor"] = dict(classroom.professor)
    c["students"] = []

    for student in classroom.students:
        c["students"].append(dict(student))

    print("DEBUG: ", c)
    classrooms.insert_one(c)

# Put
@router.put("/{id}")
async def put_classroom(id: str, classroom: Classroom):
    classrooms.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(classroom)})

# Delete
@router.delete("/{id}")
async def delete_classroom(id: str):
    classrooms.find_one_and_delete({"_id": ObjectId(id)})

    