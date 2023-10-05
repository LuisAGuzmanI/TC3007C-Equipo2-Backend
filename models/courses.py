from pydantic import BaseModel
from typing import List

from models.users import User

class Course(BaseModel):
    students: List[User]
    professor: User
    location: str
    name: str