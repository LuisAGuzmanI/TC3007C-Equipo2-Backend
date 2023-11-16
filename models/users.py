from pydantic import BaseModel
from typing import List

class User(BaseModel):
    user_id: str
    name: str
    email: str
    role: str

class EnrolledClass(BaseModel):
    date: str
    participations: int
    assistance: bool

class EnrolledCourses(BaseModel):
    professor: User
    location: str
    name: str
    participations: int
    assistance: bool
    classes: List[EnrolledClass]

class Student(User):
    enrolled_courses: List[EnrolledCourses]