from fastapi import APIRouter

from models.courses import Course
from config.database import courses
from schema.schemas import list_serial, individual_serial
from bson import ObjectId

router = APIRouter()

# Get
@router.get("/all")
async def get_all_courses():
    return list_serial(courses.find())

@router.get("/by-professor/{professor_id}")
async def get_courses_by_professor(professor_id: str):
    return list_serial(courses.find({'professor.user_id': professor_id}))

@router.get("/by-id/{id}")
async def get_courses_by_id(id: str):
    return individual_serial(courses.find_one({'_id': ObjectId(id)}))

# Post
@router.post("/")
async def post_course(course: Course):
    c = dict(course)
    c["professor"] = dict(course.professor)
    c["students"] = []

    for student in course.students:
        c["students"].append(dict(student))
        
    courses.insert_one(c)

# Put
@router.put("/{id}")
async def put_course(id: str, course: Course):
    courses.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(course)})

# Delete
@router.delete("/{id}")
async def delete_course(id: str):
    courses.find_one_and_delete({"_id": ObjectId(id)})

    