import cv2
import os

video_path = r'C:\Users\alber\Desktop\Alberto\Reto IA\OpenCV\Face Recognition\data\input\prueba.mp4'

output_directory = r'C:\Users\alber\Desktop\Alberto\Reto IA\OpenCV\Face Recognition\data\train'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haar_face.xml')

cap = cv2.VideoCapture(video_path)

image_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        face_image = frame[y:y+h, x:x+w]
        image_filename = os.path.join(output_directory, f'captured_image_{image_count}.png')
        cv2.imwrite(image_filename, face_image)

        image_count += 1

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()