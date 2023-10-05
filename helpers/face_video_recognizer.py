import os
import cv2 as cv
import numpy as np

def face_recognizer():
    # Cargamos el clasificador pre-entrenado de rostros
    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    # Cargamos el reconocedor de rostros entrenado
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.read('face_trained.yml')

    # Creamos una lista de nombres de personas
    people = []
    DIR = r'C:\Users\alber\Desktop\Alberto\Reto IA\OpenCV\Face Recognition\data\train'

    for i in os.listdir(DIR):
        people.append(i)

    # Inicializamos la captura de video de una grabación
    video_path = 'C:\\Users\\alber\\Desktop\\Alberto\\Reto IA\\OpenCV\\Face Recognition\\data\\input\\prueba_reconocimiento_2.mp4'
    output_path = r'C:\Users\alber\Desktop\Alberto\Reto IA\OpenCV\Face Recognition\data\outputs'
    cap = cv.VideoCapture(video_path)

    # Obtenemos las propiedades del video
    fps = int(cap.get(cv.CAP_PROP_FPS))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Obtenemos el nombre del video original sin la extensión de la ruta
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Definimos el codec y creamos un objeto VideoWriter
    fourcc = cv.VideoWriter.fourcc(*'XVID')
    output_file_name = f'{output_path}\output_{video_name}.avi'
    out = cv.VideoWriter(output_file_name, fourcc, fps, (width, height))

    while True:
        # Leemos un frame de la captura de video
        ret, frame = cap.read()

        if not ret:
            break

        # Convertimos el frame a escala de grises para reconocimiento facial
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detectamos posibles rostros en el frame
        faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        for (x, y, w, h) in faces_rect:
            # Extraemos la región de interés del rostro (face ROI)
            faces_roi = gray[y:y + h, x:x + w]

            # Reconocemos el rostro
            label, confidence = face_recognizer.predict(faces_roi)

            # Verificamos si el nivel de confianza se encuentra debajo del límite (se ajusta conforme se necesite)
            if confidence < 100:
                name = people[label]
            else:
                name = "Unknown"

            # Draw a rectangle around the face and display the name
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
            cv.putText(frame, name, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), thickness=2)

        # Escribimos el frame correspondiente con los rostros reconocidos
        out.write(frame)

        # Desplegamos el frame con las caras reconocidas
        cv.imshow('Face Recognition', frame)

        # Rompemos el ciclo cuando se presione la tecla 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberamos la captura de video y cerramos todas las ventanas de OpenCV
    cap.release()
    out.release()
    cv.destroyAllWindows()
