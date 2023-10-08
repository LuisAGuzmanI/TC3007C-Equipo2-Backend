import os
import cv2 as cv
import numpy as np
import requests
from io import BytesIO

def train_facial_recognizer_model(images: list, name: str):
    haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    people = [name]

    features = []
    labels = []

    def create_train():
        for person in people:
            label = people.index(person)

            for image in images:

                gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

                faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

                for (x,y,w,h) in faces_rect:
                    faces_roi = gray[y:y+h, x:x+w]
                    features.append(faces_roi)
                    labels.append(label)

    create_train()
    print('------------------- Training Done! -------------------')

    # features = np.array(features, dtype='object')
    labels = np.array(labels)

    face_recognizer = cv.face.LBPHFaceRecognizer.create()

    # Train the Recognizer on the feature list and the labels list
    face_recognizer.train(features, labels)

    # face_recognizer.save('face_trained.yml')
    # np.save('features.npy', features)
    # np.save('labels.npy', labels)

    return face_recognizer, labels