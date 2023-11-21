import cv2
import face_recognition
import tempfile

async def assistance_system(people, known_face_encodings, input_video):
    # Convertir el UploadFile a formato de bytes
    video_bytes = await input_video.read()

    # Crear un archivo de video temporal para guardar los bytes del video
    temp_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_video_file.write(video_bytes)

    # Obtenemos el nombre de archivo del video temporal
    temp_video_path = temp_video_file.name

    cap = cv2.VideoCapture(temp_video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Process each face in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any of the known persons
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                person = people[first_match_index]
                name = person.name

                if person.name != "Unknown" and not person.assistance:
                    # Log attendance
                    # with open("attendance_log.txt", "a") as log_file:
                    #     log_file.write(f"{name} - {datetime.now()}\n")

                    # Mark attendance as taken
                    person.assistance = True

            # Draw rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw label
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


        # Display the frame with counters for each person
        for idx, person in enumerate(people):
            cv2.putText(frame, f"{person.name} Assistance: {person.assistance}", (10, 30 * (idx + 1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return people