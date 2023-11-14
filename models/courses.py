from pydantic import BaseModel
from typing import List

from models.users import User


class StudentClassData(User):
    participations: int
    attendance: bool

class StudentCourseData(User):
    participations: int
    attendance: int
    
class Class(BaseModel):
    date: str
    attendance: int
    students: List[StudentClassData]

class Course(BaseModel):
    students: List[StudentCourseData]
    professor: User
    location: str
    name: str
    emoji: str
    classes: List[Class]