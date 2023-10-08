from helpers.faces_train import train_facial_recognizer_model
from helpers.face_video_recognizer import face_video_recognizer
from fastapi import UploadFile, File

from AWS.s3 import get_from_s3

async def recognition_manager(dir: str, id: str, name: str, file: UploadFile = File(...)):

    images = get_from_s3(dir, id)

    face_recognizer, labels = train_facial_recognizer_model(images, name)

    await face_video_recognizer(face_recognizer, labels, file, name)

    return 0