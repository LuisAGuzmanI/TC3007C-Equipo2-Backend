import os
import cv2 as cv
from fastapi import UploadFile, File
from io import BytesIO
import tempfile
import numpy as np
from PIL import Image

from AWS.s3 import upload_to_s3

async def video_to_face_images(dir: str, id: str, file: UploadFile = File(...)):
    # Cargamos el clasificador pre-entrenado de rostros
    haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convertir el UploadFile a formato de bytes
    video_bytes = await file.read()

    # Crear un archivo de video temporal para guardar los bytes del video
    temp_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_video_file.write(video_bytes)

    # Obtenemos el nombre de archivo del video temporal
    temp_video_path = temp_video_file.name

    # Cargamos la captura de video de OpenCV
    video_capture = cv.VideoCapture(temp_video_path)

    # Contador para capturar multiples frames por cada rostro detectado
    image_count = 0
    # Contador de imágenes guardadas
    stored_images = 0

    # Mientras el video no termine:
    while True:
        # Leemos un frame de la captura de video
        ret, frame = video_capture.read()

        if not ret:
            break

        # Convertimos el frame a escala de grises para reconocimiento facial
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detectamos posibles rostros en el frame
        faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            if image_count % 10 == 0:
                # Dibujamos un rectángulo alrededor del rostro detectado
                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Extraemos la captura del rostro
                face_image = frame[y:y+h, x:x+w]
                # Convertimos el arreglo de Numpy a BytesIO
                image_bytes = BytesIO()
                image_pil = Image.fromarray(face_image)
                image_pil.save(image_bytes, format='PNG')
                # Resetear la posición inicial de BytesIO
                image_bytes.seek(0)
                # Incrementamos el contador de imágenes guardadas
                stored_images += 1
                # Establecemos el nombre del archivo .png
                image_file_name = str(f'captured_image_{stored_images}.png')
                # Subimos la imagen al bucket de S3 en AWS
                print(upload_to_s3(dir, id, image_bytes, image_file_name))
            
            image_count += 1

    # Cerramos las ventanas
    video_capture.release()
    cv.destroyAllWindows()
    temp_video_file.close()

    os.unlink(temp_video_path)

    return {"message": "Face data saved successfully", "Amount of images": stored_images}