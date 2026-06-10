# 

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('add/', views.addStudent, name='addStudent'),
    path('students/', views.studentList, name='studentList'),
    path('search/', views.studentSearch, name='studentSearch'),

    path('details/<int:id>/', views.studentDetails, name='studentDetails'),

    path('delete/<int:id>/', views.deleteStudent, name='deleteStudent'),
    path('edit/<int:id>/', views.editStudent, name='editStudent'),
    path('update/<int:id>/', views.updateStudent, name='updateStudent'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('attendance/add/', views.addAttendance, name='addAttendance'),
    path('attendance/history/<int:student_id>/', views.attendanceHistory, name='attendanceHistory'),
]