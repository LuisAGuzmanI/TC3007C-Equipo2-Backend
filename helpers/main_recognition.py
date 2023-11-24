from helpers.face_video_recognizer import assistance_system
from helpers.pose_video_recognizer import participation_system
from helpers.Person import Person

from AWS.s3 import s3_download

async def recognition_manager(data, file):
    images = []

    for student_key, student in data.items():
        id = student['id']
        file_path = f'users/{id}/{id}.png'

        image = s3_download(key=file_path)
        images.append(image)
    
    people = []
    known_face_encodings = []
    idx = 0

    for person_key, person_info in data.items():
        name = person_info['name']
        person_id = person_info['id']
        img = images[idx]
        idx += 1

        person = Person(name, person_id, img)
        people.append(person)
        known_face_encodings.append(person.person_face_encoding)

    # people = await assistance_system(people, known_face_encodings, file)

    people = await participation_system(people, known_face_encodings, file)

    people_data = {}

    for person in people:
        person_info = {
            'name': person.name,
            'id': person.id,
            'attendance': person.assistance,
            'participations': person.participations
        }

        people_data[person.id] = person_info

    return people_data