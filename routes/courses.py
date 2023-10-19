from fastapi import APIRouter, UploadFile, File
import random

from models.courses import Course, StudentClassData
from config.database import courses
from typing import List
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

"""
Metodos de clases
"""
# TODO: Hacer que esta información en lugar de ser random se genere con el reconocimiento de video
@router.post("/add-class/{id}")
async def post_course(id:str, date: str, file: UploadFile = File(...)):
    course = individual_serial(courses.find_one({'_id': ObjectId(id)}))
    _class = {
        "date": date,
        "attendance": 0,
        "students": []
    }

    for student in course['students']:
        participations = random.randint(0, 5)
        attendance = random.random() < 0.8
        attendance_increment = 1 if attendance else 0

        courses.update_one(
            { "_id": ObjectId(id), "students.user_id": student['user_id'] }, 
            { 
                "$inc": { "students.$.participations": participations, "students.$.attendance": attendance_increment }
            }
        )

        student['participations'] = participations
        student['attendance'] = attendance

        _class['students'].append(student)

    courses.update_one(
        { "_id": ObjectId(id) },
        {
            "$push": { "classes": _class }
        }
    )

    