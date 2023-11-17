from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from routes.courses import router as courses_router


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])    