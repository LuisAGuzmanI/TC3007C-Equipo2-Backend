from fastapi import APIRouter, UploadFile, File, HTTPException
import random

from project_models.courses import Course, StudentClassData
from config.database import courses
from typing import List
from schema.schemas import list_serial, individual_serial
from bson import ObjectId
from datetime import datetime

from helpers.main_recognition import recognition_manager

router = APIRouter()

# Get
@router.get("/all")
async def get_all_courses():
    return list_serial(courses.find())

@router.get("/by-professor/{professor_id}")
async def get_courses_by_professor(professor_id: str):
    return list_serial(courses.find({'professor.user_id': professor_id}))

@router.get("/by-id/{id}")
async def get_courses_by_id(id: str):
    return individual_serial(courses.find_one({'_id': ObjectId(id)}))

# Post
@router.post("/")
async def post_course(course: Course):
    c = dict(course)
    c["professor"] = dict(course.professor)
    c["students"] = []

    for student in course.students:
        c["students"].append(dict(student))
        
    courses.insert_one(c)

# Put
@router.put("/{id}")
async def put_course(id: str, course: Course):
    courses.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(course)})

# Delete
@router.delete("/{id}")
async def delete_course(id: str):
    courses.find_one_and_delete({"_id": ObjectId(id)})

"""
Metodos de clases
"""
# TODO: Hacer que esta información en lugar de ser random se genere con el reconocimiento de video
@router.post("/add-class/{id}/{date}")
async def post_class(id:str, date: str, file: UploadFile = File(...)):
    course = individual_serial(courses.find_one({'_id': ObjectId(id)}))

    students_data = {
        'person_1' : {
            'id': 1,
            'name': 'Alberto Orozco',
        },
        'person_2' : {
            'id': 2,
            'name': 'Alonso Orozco',
        }
    }

    students_results = await recognition_manager(students_data, file)

    print(students_results)

    raise HTTPException(status_code=404, detail=f"Early termination. TEST")

    
    # Extract the date and time without timezone information
    date_str_no_timezone = date[:24]

    # Parse the date string
    date_obj = datetime.strptime(date_str_no_timezone, "%a %b %d %Y %H:%M:%S")

    # # Format the date as dd/mm/yyyy
    formatted_date = date_obj.strftime("%d/%m/%Y")

    _class = {
        "id": id + "_" + str(len(course["classes"])) + "_" + date_obj.strftime("%d-%m-%Y"),
        "date": formatted_date,
        "attendance": 0,
        "participations": 0,
        "students": []
    }

    for student in course['students']:
        participations = random.randint(0, 5)
        attendance = random.random() < 0.8
        attendance_increment = 1 if attendance else 0
        courses.update_one(
            { "_id": ObjectId(id), "students.user_id": student['user_id'] }, 
            { 
                "$inc": { "students.$.participations": participations, "students.$.attendance": attendance_increment }
            }
        )

        student['participations'] = participations
        student['attendance'] = attendance

        _class['attendance'] += attendance
        _class['participations'] += participations
        _class['students'].append(student)

    courses.update_one(
        { "_id": ObjectId(id) },
        {
            "$push": { "classes": _class }
        }
    )

    
@router.put("/update-class-info/{course_id}/{class_id}/{user_id}/{field}/{value}")
async def update_class_info(course_id: str, class_id: str, user_id: str, field: str, value: int):

    if field == "participations":
        course = courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
        
        target_class = next((cls for cls in course['classes'] if cls['id'] == class_id), None)
        if not target_class:
            raise HTTPException(status_code=404, detail=f"Class {class_id} not found in course {course_id}")
        
        target_student = next((student for student in target_class['students'] if student['user_id'] == user_id), None)
        if not target_student:
            raise HTTPException(status_code=404, detail=f"Student {user_id} not found in class {class_id}")
        
        current_participations = target_student.get('participations')

    # ACTUALIZACIÓN DEL ALUMNO EN EL ARREGLO DE 'CLASSES'

    # Define the update query
    update_query_class_students = {
        "_id": ObjectId(course_id),
        "classes": {
            "$elemMatch": {"id": class_id}
        },
        "classes.students.user_id": user_id
    }

    # Define the update operation based on the field parameter
    if field == "participations":
        update_operation_class = {
            "$set": {
                "classes.$[class].students.$[student].participations": value
            }
        }
    elif field == "attendance":
        update_operation_class = {
            "$set": {
                "classes.$[class].students.$[student].attendance": True if value else False
            }
        }
    else:
        raise HTTPException(status_code=400, detail=f"Invalid field parameter. Use 'participations' or 'attendance'.")

    # Define the array filter for the positional operator
    array_filters_class = [
        {"class.id": class_id},
        {"student.user_id": user_id}
    ]

    # Perform the update operation
    result_class_students = courses.update_one(update_query_class_students, update_operation_class, array_filters=array_filters_class)    

    if result_class_students.modified_count < 1 :
        raise HTTPException(status_code=404, detail=f"Student class info was not updated")

    # ACTUALIZACIÓN DEL ALUMNO EN EL ARREGLO DE 'STUDENTS'

    # Define the update query for the course students
    update_query_course_students = {
        "_id": ObjectId(course_id),
        "students.user_id": user_id
    }

    # Define the update operation for the course students based on the field parameter
    if field == "participations":
        update_operation_course_students = {
            "$inc": {
                "students.$.participations":  value - current_participations
            }
        }
    elif field == "attendance" and value:
        update_operation_course_students = {
            "$inc": {
                "students.$.attendance": 1 
            }
        }
    elif field == "attendance" and not value:
        update_operation_course_students = {
            "$inc": {
                "students.$.attendance": -1 
            }
        }
    else:
        raise HTTPException(status_code=400, detail=f"Invalid field parameter. Use 'participations' or 'attendance'.")

    # Perform the update operation for the course students
    result_course_students = courses.update_one(update_query_course_students, update_operation_course_students)

    if result_course_students.modified_count < 1 :
        raise HTTPException(status_code=404, detail=f"Student {user_id} course info was not updated")
    
    # ACTUALIZACIÓN DE LA INFORMACIÓN DEL OBJETO CLASS
    
    update_query_class_info = {
        "_id": ObjectId(course_id),
        "classes": {
            "$elemMatch": {"id": class_id}
        }
    }

    if field == "participations":
        update_operation_class_info = {
            "$inc": {
                "classes.$.participations":  value - current_participations
            }
        }
    elif field == "attendance" and value:
        update_operation_class_info = {
            "$inc": {
                "classes.$.attendance": 1 
            }
        }
    elif field == "attendance" and not value:
        update_operation_class_info = {
            "$inc": {
                "classes.$.attendance": -1 
            }
        }
    else:
        raise HTTPException(status_code=400, detail=f"Invalid field parameter. Use 'participations' or 'attendance'.")
    
    result_class_info = courses.update_one(update_query_class_info, update_operation_class_info)

    if result_class_info.modified_count < 1 :
        raise HTTPException(status_code=404, detail=f"Class info was not updated")
    
    return {"message": "Student info was updated successfully."}, 200

@router.get("/total-classes/{course_id}")
async def get_total_classes(course_id: str):
    # Define the query to find the course by its ID
    query = {"_id": ObjectId(course_id)}

    # Retrieve the course document
    course = courses.find_one(query)

    if course:
        # Get the classes array and return its length
        classes = course.get('classes', [])
        return len(classes)
    else:
        HTTPException(status_code=404, detail=f"Course id is not valid")

@router.get("/average-attendance/{course_id}")
def get_average_attendance(course_id):
    # Define the query to find the course by its ID
    query = {"_id": ObjectId(course_id)}

    # Retrieve the course document
    course = courses.find_one(query)

    if course:
        # Get the classes array
        classes = course.get('classes', [])

        # Calculate total assistances and total number of classes
        total_assistances = sum(cls['attendance'] for cls in classes)
        total_classes = len(classes)

        if total_classes > 0:
            # Calculate and return the average
            average_assistances = round(total_assistances / total_classes, 2)
            return average_assistances
        else:
            return 0  # No classes available
    else:
        HTTPException(status_code=404, detail=f"Course id is not valid")

@router.get("/average-participations/{course_id}")
def get_average_participations(course_id):
    # Define the query to find the course by its ID
    query = {"_id": ObjectId(course_id)}

    # Retrieve the course document
    course = courses.find_one(query)

    if course:
        # Get the classes array
        classes = course.get('classes', [])

        # Calculate total assistances and total number of classes
        total_participations = sum(cls['participations'] for cls in classes)
        total_classes = len(classes)

        if total_classes > 0:
            # Calculate and return the average
            average_assistances = round(total_participations / total_classes, 2)
            return average_assistances
        else:
            return 0  # No classes available
    else:
        HTTPException(status_code=404, detail=f"Course id is not valid")

@router.get("/courses-by-student/{student_id}")
def get_courses_by_student(student_id):
    # Define the query to find the course by its ID
    query = {"students.user_id": student_id}

    # Retrieve the course document
    found_courses = courses.find(query)

    results = []

    if found_courses:
        for course in found_courses:
            course_id = str(course['_id'])
            total_attendance = 0
            total_participations = 0

            # Iterate over classes in the course
            for class_info in course.get('classes', []):
                # Iterate over students in the class
                for student_info in class_info.get('students', []):
                    if student_info['user_id'] == student_id:
                        # Accumulate attendances and participations
                        total_attendance += 1 if student_info['attendance'] else 0
                        total_participations += student_info['participations']

            # Add results to the dictionary
            results.append({
                'total_attendance': total_attendance,
                'total_participations': total_participations,
                'course_id': course_id,
                'course_name': course['name'],
                'course_location': course['location'],
                'course_emoji': course['emoji'],
                'course_professor': course['professor']['name'],
            })

        return results
    else:
        HTTPException(status_code=404, detail=f"The student was not found in any course")

