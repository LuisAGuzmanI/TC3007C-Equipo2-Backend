from helpers.faces_train import train_facial_recognizer_model

from AWS.s3 import get_from_s3

async def recognition_manager(dir: str, id: str, name: str):

    images = get_from_s3(dir, id)

    print(images)

    # train_facial_recognizer_model(images, name)

    return 0