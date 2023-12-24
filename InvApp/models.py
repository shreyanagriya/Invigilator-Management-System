from enum import unique
from random import choices
from tkinter import N
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Notice Model
class Notice(models.Model):
    image = models.ImageField(upload_to='notice_images', null=True, blank=True)
    title = models.TextField(max_length=400)
    description = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def get_first_100_chars(self):  
        if len(self.title) <= 100:
            return self.title
        else:
            return self.title[:100] + '...'

    def __str__(self):
        return self.get_first_100_chars()


# Tracher Model

class Teacher (models.Model):
    choice = (
        ('Yes', 'Chairman'),
        ('No', 'Just a Teacher')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, null=True, unique=True)
    designation = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default='images/default_image.png')
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Student Model


class Student(models.Model):
    BATCH = (
        ("48", "48"),
        ("47", "47"),
        ("49", "49"),
        ("50", "50"),
        ("51", "51"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    registration_number = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    batch = models.CharField(default='48', max_length=30, blank=True, null=True, choices=BATCH)
    image = models.ImageField(upload_to='images/', default='images/default_image.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Course (models.Model):
    course_name = models.CharField(max_length=200, null=True, unique=True)
    course_teacher = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.course_name


class Exam(models.Model):
    subject = models.OneToOneField(Course, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    exam_time = models.TimeField(null=True)
    teachers = models.ManyToManyField(Teacher, null=True)


    def __str__(self):
        return self.subject.course_name


class Semester (models.Model):
    semester_name = models.CharField(null=True, max_length=200)
    student_number = models.PositiveIntegerField()
    courses = models.ManyToManyField(Course, null=True)
    chairman = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.semester_name)
    
class Routine (models.Model):
    exams = models.ManyToManyField(Exam, null=True)
    semester = models.OneToOneField(Semester,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.semester)



