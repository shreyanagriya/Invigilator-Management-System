from audioop import reverse
from pyexpat.errors import messages
from urllib import request
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, View, CreateView, DeleteView,FormView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

class AdminRequiredMixin(object):
    """
    Mixin to restrict access to admin-only views.
    """

    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return user_passes_test(lambda u: u.is_superuser)(view)

def handler404(request, exception):
    return render(request, 'inv/404.html', status=404)

class AdminPageView(AdminRequiredMixin,TemplateView):
    template_name = "inv/admin_pages.html"

class NoticeCreateView(AdminRequiredMixin,CreateView):
    template_name = "create/notice_form.html"
    form_class = noticeBuildForm
    success_url = reverse_lazy('index')

class NoticeDeleteView(AdminRequiredMixin,LoginRequiredMixin, DeleteView):
    model = Notice
    success_url = reverse_lazy('index')
    template_name = 'inv/notice_confirm_delete.html'

def delete_notice(request, id):
    notice = get_object_or_404(Notice, id=id)

    if request.method == 'POST':
        notice.delete()
        return redirect('index')

    context = {'notice': notice}
    return render(request, 'inv/notice_confirm_delete.html', context)

class SemesterCreateView(AdminRequiredMixin,CreateView):
    template_name = 'create/semester_form.html'
    form_class = SemesterForm
    success_url = reverse_lazy('index')

class RoutineCreateView(AdminRequiredMixin,CreateView):
    template_name = 'create/routine_form.html'
    form_class = RoutineForm
    success_url = reverse_lazy('index')

class indexView(TemplateView):
    template_name = "inv/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_Notice = Notice.objects.all().order_by('-id')
        paginator = Paginator(all_Notice, 3)
        page_number = self.request.GET.get('page')
        notices = paginator.get_page(page_number)
        context['notices'] = notices
        return context
    


def all_Notice(request):
    context = {'notices': Notice.objects.all().order_by("-id")}
    # context['habijabi'] = Notice.objects.all()
    return render(request, 'notice/allnotice.html', context)


class NoticeDetailView(View):
    def get(self, request, *args, **kwargs):
        notice = get_object_or_404(Notice, pk=kwargs['id'])
        context = {'notice': notice}
        return render(request, 'notice/notice_detail.html', context)

# @user_passes_test(lambda u: u.is_superuser)


class NoticeUpdateView(AdminRequiredMixin, UpdateView):
    model = Notice
    fields = ['image', 'title', 'description']
    template_name = 'notice/notice_form.html'
    success_url = reverse_lazy('allnotice')
    context_object_name = 'notice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

# @login_required

# Semester's Related View Function

def view_semester(request, LoginRequiredMixin):

    teachers_count = Exam.teachers.through.objects.values(
        'teacher').annotate(count=Count('teacher')).order_by('count')

    for item in teachers_count:
        teacher_name = Teacher.objects.get(pk=item['teacher']).short_name
        count = item['count']
        print(f"{teacher_name} - {count}")
    return render(request, 'inv/viewemny.html')

class SemesterDetailView(LoginRequiredMixin, TemplateView):
    template_name = "inv/selected_teacher_sem.html"
    login_url = "stu_login"

    def get(self, request):
        semesters = Semester.objects.all()
        semester_list = []
        for semester in semesters:
            semester_list.append({
                'name': semester.semester_name,
                'url': reverse_lazy('viewsemester', args=[semester.semester_name])
            })
        return render(request, self.template_name, {'semester_list': semester_list})


class EachSemesterView(LoginRequiredMixin, DetailView):
    login_url = 'stu_login'
    model = Semester
    template_name = 'inv/view_semester.html'
    context_object_name = 'semester'
    def get_object(self, queryset=None):
        semester_name = self.kwargs['semester_name']
        return get_object_or_404(Semester, semester_name=semester_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        semester = self.object
        routine = get_object_or_404(Routine, semester=semester)
        selected_exams = routine.exams.all()
        context['exams'] = selected_exams
        return context
    # def get(self, request, semester_name):
    #     semester = Semester.objects.get(semester_name=semester_name)
    #     final_routine = semester.final_routine
    #     selected_exams = Routine.exams.all()
    #     print(selected_exams)
    #     selected_teachers = Teacher.objects.filter(exam__in=selected_exams)
    #     print(selected_teachers)

    #     print(semester)
    #     return render(request, 'inv/view_semester.html',
    #                   {'semester_name': semester_name, "semester": Semester.objects.all(), 'exams': selected_exams, 'teachers': selected_teachers})


class CommitteListView(LoginRequiredMixin, TemplateView):
    template_name = "inv/view_commite_list.html"
    login_url = "teach_login"

    def get(self, request):
        semesters = Semester.objects.all()
        return render(request, self.template_name, {'semesters': semesters})

class CourseCreateView(AdminRequiredMixin, CreateView):
    template_name = 'create/create_course.html'
    form_class = CourseCreationForm
    success_url = reverse_lazy('index')


#Routine Related View Functin

class CreateRoutine(AdminRequiredMixin, View):

    def get(self, request, semester_name):
        semester = Semester.objects.get(semester_name=semester_name)
        form = RoutineCreationForm(semester_name=semester_name)
        return render(request, 'create/create_routine.html', {'semester': semester, 'form': form, "sem_object": Semester.objects.all(), 'semester_name': semester_name})

    def post(self, request, semester_name):
        semester = Semester.objects.get(semester_name=semester_name)
        form = RoutineCreationForm(request.POST, semester_name=semester_name)
        if form.is_valid():
            routine = form.save()
            routine.save()
            semester.routine = routine
            semester.save()
            return redirect('index')
        return render(request, 'create/create_routine.html', {'semester': semester,
                                                           'form': form, "sem_object": Semester.objects.all()})


class ExamRoutine(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "inv/exam_routine.html"
    
    def get(self, request):
        semesters = Semester.objects.all()
        semester_list = []
        for semester in semesters:
            semester_list.append({
                'name': semester.semester_name,
                'url': reverse_lazy('createroutine', args=[semester.semester_name])
            })
    
        
        return render(request, self.template_name, {'semester_list': semester_list})



# Teacher Related


class TeacherRegistrationView(CreateView):
    template_name = "teacher/teach_register.html"
    form_class = TeacherForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            form.add_error(None, "Username or email already exists.")
            return self.form_invalid(form)

        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    fields = ['first_name', 'last_name', 'short_name', 'designation','image']
    template_name = 'teacher/edit_teacher.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Teacher, id=id)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def clean_short_name(self):
        short_name = self.cleaned_data.get('short_name')
        if Teacher.objects.filter(short_name=short_name).exists():
            raise forms.ValidationError("Short Name already exists.")
        return short_name
    
    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.object.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)

class TeacherLoginView(FormView):
    template_name = "teacher/teach_login.html"
    form_class = teacherLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        passwrd = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=passwrd)
        if usr is not None and Teacher.objects.filter(user=usr).exists():
            login(self.request, usr)
            # request.session['teacherlogin'] = True
        else:
            return render(self.request, self.template_name, {"form": self.form_class,
                                                             "error": "Invalid  Credentials !!"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
        
#Profile view

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "inv/profile_detail.html"
    login_url = 'stu_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        user = User.objects.filter(username=username).first()
        if hasattr(user, 'teacher'):
            teacher = user.teacher
            exam = Exam.objects.filter(teachers=teacher)
            context['exams'] = exam
        context['user'] = user
        return context
    
#Student Related

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['registration_number', 'first_name', 'last_name', 'batch', 'image']
    template_name = 'student/edit_student.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Student, id=id)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def clean_registration_number(self):
        registration_number = self.cleaned_data.get('registration_number')
        if Student.objects.filter(registration_number=registration_number).exists():
            raise forms.ValidationError("Registration number already exists.")
        return registration_number
    
    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.object.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)



# Student Login Form

class StudentLoginView(FormView):
    template_name = "student/stu_login.html"
    form_class = studentLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        passwrd = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=passwrd)
        if usr is not None and Student.objects.filter(user=usr).exists():
            login(self.request, usr)
            # request.session['studentlogin'] = True
        else:
            return render(self.request, self.template_name, {"form": self.form_class,
                                                             "error": "Invalid  Credentials !!"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url



class StudentRegistrationView(CreateView):
    template_name = "student/stu_register.html"
    form_class = StudentForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        # Check if user with the same username or email already exists
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            form.add_error(None, "Username or email already exists.")
            return self.form_invalid(form)

        # Create a new user
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

# Logout Buttons

def student_logout(request):
    logout(request)
    return redirect('index')


def teacher_logout(request):
    del request.session['teacherlogin']
    return redirect('teach_login')
