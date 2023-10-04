from pydantic import BaseModel
from typing import List

from models.users import User

class Classroom(BaseModel):
    students: List[User]
    professor: User
    location: str