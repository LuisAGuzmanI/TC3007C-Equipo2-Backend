import face_recognition

class Person():
    def __init__(self, name="", id=0, img=None, assistance=False, participations=0, arm_raised=False):
        # Student parameters
        self.name = name
        self.id = id
        self.img = img
        self.assistance = assistance
        self.participations = participations
        self.arm_raised = arm_raised

        # Facial Model Encoding
        self.person_face_encoding = face_recognition.face_encodings(self.img)[0]