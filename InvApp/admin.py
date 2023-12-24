from django.contrib import admin
from .models import  Semester, Student, Teacher,Notice,Course,Routine,Exam
# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Notice)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Routine)
admin.site.register(Exam)
