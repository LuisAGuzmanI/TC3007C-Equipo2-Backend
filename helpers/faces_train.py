import os
import cv2 as cv
import numpy as np
import requests
from io import BytesIO

def train_facial_recognizer_model(image_urls: list, name: str):
    haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    people = [name]

    features = []
    labels = []

    def create_train():
        for person in people:
            label = people.index(person)

            for img_url in image_urls:
                # Descargamos la imagen desde la URL
                response = requests.get(img_url)

                # Verificamos si la petición fue exitosa
                if response.status_code == 200:
                    img_array = cv.imdecode(np.frombuffer(response.content, np.uint8), cv.IMREAD_COLOR)
                    print(img_array)

                    gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

                    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

                    for (x,y,w,h) in faces_rect:
                        faces_roi = gray[y:y+h, x:x+w]
                        features.append(faces_roi)
                        labels.append(label)
                else:
                    print(f"Failed to download image from URL: {img_url}")

    create_train()
    print('------------------- Training Done! -------------------')

    features = np.array(features, dtype='object')
    labels = np.array(labels)

    face_recognizer = cv.face.LBPHFaceRecognizer.create()

    # Train the Recognizer on the feature list and the labels list
    face_recognizer.train(features, labels)

    face_recognizer.save('face_trained.yml')
    np.save('features.npy', features)
    np.save('labels.npy', labels)