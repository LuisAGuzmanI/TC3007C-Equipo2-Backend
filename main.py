from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from routes.classrooms import router as classrooms_router


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",  # Add the URL of your Vue.js application
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(classrooms_router, prefix="/classrooms", tags=["classrooms"])    