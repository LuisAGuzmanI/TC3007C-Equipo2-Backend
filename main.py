from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from routes.courses import router as courses_router


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",  # Development enviorment
    "http://localhost:4173",  # Build preview enviorment
    "http://127.0.0.1:8000",  # Production backend gateway delopyment
    "https://main.d2qq7id2kqiuhj.amplifyapp.com",  # Production frontend delopyment
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