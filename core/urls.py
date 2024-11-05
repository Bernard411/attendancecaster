from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView



from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home-page'),
    path('recognize/', views.recognize, name='recognize'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('add_attendance/', views.add_attendance, name='add_attendance'),
    path('attendance_table/', views.attendance_table, name='attendance_table'),
    path('timetable/', views.timetable, name='timetable'),
   
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

