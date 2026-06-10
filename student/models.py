from django.db import models

# Create your models here.

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10, unique=True)
    branch = models.CharField(max_length=50)
    year = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=10)

class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.student_name} - {self.date}"
    
    class Meta:
        unique_together = ('student', 'date')  # 🚨 NO DUPLICATES
        ordering = ['-date']
    

