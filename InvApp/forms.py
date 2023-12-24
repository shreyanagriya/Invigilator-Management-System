from itertools import chain
from django import forms
from .models import Student, Teacher, Notice

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q, Count

# Student Form


class StudentForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['registration_number', 'first_name',
                  'last_name', 'batch','image']
        labels = {
            'registration_number': 'Registration Number',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'batch': 'Select Your Batch',
            'image': 'Upload Your Image',
        }

        widgets = {
            'registration_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

        def clean_username(self):
            uname = self.cleaned_data.get("username")
            
            if User.objects.filter(username=uname).exists():
                raise forms.ValidationError("This username already exists!!")

            return uname

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')

    #     if email and Student.objects.filter(email=email):
    #         raise forms.ValidationError('This email already exists !!')
    #     return email

# Student Login Form

# Student Login Form


class studentLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Teacher Reg Form

class TeacherForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Teacher
        fields = ['first_name',
                  'last_name', 'short_name', 'designation','image']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'short_name': 'Short Name',
            'designation': 'DesigNation',
            'image': 'Upload Your Image',
        }

        widgets = {
            'teacher_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_short_name(self):
        short_name = self.cleaned_data.get('short_name')

        if short_name and Teacher.objects.filter(short_name=short_name):
            raise forms.ValidationError('This Short_name already exists !!')
        return short_name

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("This username already exists!!")

        return uname


class teacherLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class noticeBuildForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description','image']
        labels = {
            'title': 'Notice Title',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RoutineCreationForm(forms.ModelForm):
    teachers_count = Exam.teachers.through.objects.values('teacher').annotate(count=Count('teacher')).filter(count__lt=3).order_by('count')
    teacher_ids = [item['teacher'] for item in teachers_count]
    # teachers_queryset = Teacher.objects.filter(id__in=teacher_ids)
    # all_teachers_queryset = Teacher.objects.all()
    # final_queryset = teachers_queryset.union(all_teachers_queryset).distinct()
    teacher_qs = Teacher.objects.filter(id__in=teacher_ids)
    all_teachers_qs = Teacher.objects.all()

    merged_qs = list(chain(teacher_qs, all_teachers_qs))
    unique_teachers_qs = Teacher.objects.filter(id__in=[teacher.id for teacher in merged_qs])

    
    teachers = forms.ModelMultipleChoiceField(
        queryset=unique_teachers_qs,  # add comma here
        widget=forms.CheckboxSelectMultiple
    )
    def __init__(self, *args, **kwargs):
        semester_name = kwargs.pop('semester_name')
        super(RoutineCreationForm, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(
            queryset=Course.objects.filter(semester__semester_name=semester_name), 
            widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Exam
        fields = ['subject', 'date','exam_time', 'teachers']
        labels = {
            'subject': 'Subject',
            'date': 'Exam date',
            'exam_time': 'Exam Time',
            'teachers': 'Select the Teachers',
        }

        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exam_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }


class CourseCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_teacher'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
    class Meta:
        model = Course
        fields = ['course_name', 'course_teacher']
        labels = {
            'course_name': 'Coures Name',
            'course_teacher': 'Select Course Teacher',
        }

        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_teacher': forms.Select(attrs={'class': 'form-control',}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    
class RoutineForm(forms.ModelForm):
    exam_list = Exam.objects.all()
    exams = forms.ModelMultipleChoiceField(
        queryset=exam_list,  # add comma here
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Routine
        fields = ['exams', 'semester']
        labels = {
            'exams': 'Exam Name',
            'semester': 'Name the Semester',
        }

        widgets = {
            'exams': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control',}),
        }

class SemesterForm(forms.ModelForm):
    course_list = Course.objects.all()  # use Course queryset instead of Exam queryset
    courses = forms.ModelMultipleChoiceField(
        queryset=course_list,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Semester
        fields = ['semester_name', 'student_number', 'courses', 'chairman']
        labels = {
            'semester_name': 'Semester Name',
            'student_number': 'Student Number',
            'courses': 'Courses of Semester',
            'chairman': 'Select The Chairman',
        }

        widgets = {
            'semester_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_number': forms.NumberInput(attrs={'class': 'form-control',}),
            'courses': forms.SelectMultiple(attrs={'class': 'form-control',}),
            'chairman': forms.Select(attrs={'class': 'form-control',}),
        }




# Notice form

# class NoticeForm(forms.ModelForm):
#     class Meta:
#         model = Notice
#         fields = ['image', 'title', 'description']
#         labels = {
#             'image': 'Upload Image',
#             'title': 'Title of the Notice',
#             'description': 'Description of the Notice',
#         }

#         widgets = {
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control',}),
#             'description': forms.Textarea(attrs={'class': 'form-control',}),
#         }