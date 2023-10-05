from helpers.faces_train import train_facial_recognizer_model

from AWS.s3 import get_from_s3

async def recognition_manager(dir: str, id: str):

    files = get_from_s3(dir, id)

    return 0