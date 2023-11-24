import cv2
import yolov5 as yv5
import mediapipe as mp
import face_recognition
import traceback
import tempfile

async def participation_system(people, known_face_encodings, input_video):

    pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.9)

    model_path = 'helpers/yolov5s.pt'
    device = "cpu"  # for cpu
    # device = 0  # for gpu
    yolov5 = yv5.YOLOv5(model_path, device, load_on_init=True)

    # Convertir el UploadFile a formato de bytes
    video_bytes = await input_video.read()

    # Crear un archivo de video temporal para guardar los bytes del video
    temp_video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_video_file.write(video_bytes)

    # Obtenemos el nombre de archivo del video temporal
    temp_video_path = temp_video_file.name

    video_capture = cv2.VideoCapture(temp_video_path)

    # Process each frame of the video
    while True:
        # Read the next frame
        success, frame = video_capture.read()

        if frame is None:
            print("Frame is None. Exiting.")
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

        # Perform object detection on the frame
        results = yolov5.predict(frame, size=640, augment=False)
        detections = results.pred[0]

        # Check whether the bounding box centroids are inside the ROI
        for detection in detections:
            xmin = detection[0]
            ymin = detection[1]
            xmax = detection[2]
            ymax = detection[3]
            score = detection[4]
            class_id = detection[5]
            centroid_x = int(xmin + xmax) // 2
            centroid_y = int(ymin + ymax) // 2

            # Threshold score
            if score >= 0.6:
                if class_id == 0:
                    color = (255, 0, 0)
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 1)

                    # Padding
                    padding = 25
                    person_roi = frame[int(ymin):int(ymax), int(xmin):int(xmax)]

                    try:  # Mediapipe
                        # Count arm raises
                        results_pose = pose.process(person_roi)
                        if results_pose.pose_landmarks:

                            # Shoulder landmarks (left and right)
                            left_shoulder = results_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                            right_shoulder = results_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]

                            # Hand landmarks (for example, the tip of the index finger)
                            left_hand = results_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_INDEX]
                            right_hand = results_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_INDEX]

                            # Pose tracking logic (same as in your original script)
                            left_arm_landmarks = results_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER:mp.solutions.pose.PoseLandmark.LEFT_WRIST]
                            right_arm_landmarks = results_pose.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER:mp.solutions.pose.PoseLandmark.RIGHT_WRIST]

                            left_arm_average_y = sum(point.y for point in left_arm_landmarks) / len(left_arm_landmarks)
                            right_arm_average_y = sum(point.y for point in right_arm_landmarks) / len(right_arm_landmarks)

                            left_arm_up = left_arm_average_y < left_arm_landmarks[0].y
                            right_arm_up = right_arm_average_y < right_arm_landmarks[0].y

                            # Check if the person is participating based on hand positions
                            not_participating = left_hand.y < left_shoulder.y and right_hand.y < right_shoulder.y

                            rgb_roi = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)

                            # cv2.imshow("Detected participation", rgb_roi)
                            # cv2.waitKey(0)

                            if rgb_roi.any():
                                rgb_encoding = face_recognition.face_encodings(rgb_roi)[0]

                                # print(f"left hand: {left_hand}, right_hand: {right_hand}")

                                matches = face_recognition.compare_faces(known_face_encodings, rgb_encoding, tolerance=0.48)

                                if True in matches:
                                    idx = matches.index(True)

                                    if people[idx].arm_raised == False and (left_arm_up or right_arm_up) and not not_participating:
                                            people[idx].participations += 1
                                            people[idx].arm_raised = True
                                            print(f"Participation Registered for {people[idx].name}")

                                    elif people[idx].arm_raised == True and not (left_arm_up or right_arm_up) and not_participating:
                                            print(f"{people[idx].name}'s arm down")
                                            people[idx].arm_raised = False

                    except Exception as e:
                        print(f"Error processing image: {e}")
                        print(traceback.format_exc())

                else:
                    pass

        # Display the frame with counters for each person
        for idx, person in enumerate(people):
            cv2.putText(frame, f"{person.name}: {person.participations} participations", (10, 30 + 20 * idx),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)

        # Display the frame
        # cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    video_capture.release()

    cv2.destroyAllWindows()

    return people