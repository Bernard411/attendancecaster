from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

import base64
import cv2
import numpy as np
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Attendance
from django.utils import timezone
import face_recognition
import base64
import cv2
import numpy as np
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Attendance
from django.utils import timezone
import face_recognition

import base64
import numpy as np
import cv2
import face_recognition
from django.http import JsonResponse
from .models import Student, Attendance
from datetime import date
import json
from io import BytesIO
from PIL import Image

def recognize(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            image = np.array(Image.open(BytesIO(base64.b64decode(image_data))))

            # Detect faces and encode the captured image
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if face_encodings:
                students = Student.objects.all()
                known_encodings = [np.frombuffer(student.face_encoding, dtype=np.float64) for student in students]
                known_ids = [student.id for student in students]

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding)
                    if True in matches:
                        match_index = matches.index(True)
                        student_id = known_ids[match_index]
                        student = Student.objects.get(id=student_id)

                        # Mark attendance
                        subject = Subject.objects.first()  # Example subject
                        Attendance.objects.get_or_create(
                            student=student,
                            subject=subject,
                            date=date.today(),
                            defaults={'status': True}
                        )
                        return JsonResponse({'message': f'Attendance marked for {student.name}'})

            return JsonResponse({'message': 'No match found'})

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Subject, Attendance
from django.contrib.auth.models import User

# View to add a student
def add_student(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        name = request.POST['name']
        roll_number = request.POST['roll_number']
        image = request.FILES['image']

        user = User.objects.get(id=user_id)
        student = Student.objects.create(user=user, name=name, roll_number=roll_number, image=image)
        return redirect('add_student')
    users = User.objects.all()
    return render(request, 'add_student.html', {'users': users})

# View to add a subject
def add_subject(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']

        Subject.objects.create(name=name, code=code)
        return redirect('add_subject')
    return render(request, 'add_subject.html')

# View to add attendance
def add_attendance(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        subject_id = request.POST['subject_id']
        date = request.POST['date']
        status = request.POST.get('status') == 'on'

        student = Student.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)
        Attendance.objects.create(student=student, subject=subject, date=date, status=status)
        return redirect('add_attendance')
    students = Student.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'add_attendance.html', {'students': students, 'subjects': subjects})


from django.shortcuts import render
from .models import Attendance, Subject

# View to display attendance records
def attendance_table(request):
    attendances = Attendance.objects.all().order_by('date')
    return render(request, 'attendance_table.html', {'attendances': attendances})

# View to display timetable (assuming it’s subject-based for simplicity)
def timetable(request):
    subjects = Subject.objects.all()
    return render(request, 'timetable.html', {'subjects': subjects})
