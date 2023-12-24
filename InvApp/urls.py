
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('', views.indexView.as_view(), name='index'),


    path('studentregister/', views.StudentRegistrationView.as_view(),
         name='stu_register'),
    path('teacherregister/', views.TeacherRegistrationView.as_view(),
         name='teach_register'),

    path('studentlogin/', views.StudentLoginView.as_view
         (template_name='student/stu_login.html'), name='stu_login'),

    path('logout/', views.student_logout, name='logout'),

    path('teacherlogin/', views.TeacherLoginView.as_view(template_name='teacher/teach_login.html'), name='teach_login'),
    path('createroutine/<str:semester_name>/',
         views.CreateRoutine.as_view(), name='createroutine'),
    
    path('examroutine/', views.ExamRoutine.as_view(), name='examroutine'),
    path('cratecourse/', views.CourseCreateView.as_view(), name='cratecourse'),
    path('viewallsemester/', views.SemesterDetailView.as_view(), name='viewallsemester'),

    path('viewsemester/<str:semester_name>/', views.EachSemesterView.as_view(), name='viewsemester'),

    path('notice/<int:id>/', views.NoticeDetailView.as_view(), name='notice_detail'),
#     path('noticeupdate/<int:id>/', views.NoticeUpdateView.as_view(), name='noticeupdate'),
    path('notice/<int:pk>/update/', views.NoticeUpdateView.as_view(), name='notice_update'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('edit-student/<int:id>/', views.StudentUpdateView.as_view(), name='edit_student'),
    path('edit-teacher/<int:id>/', views.TeacherUpdateView.as_view(), name='edit_teacher'),


#     path('teacherlogout/', views.teacher_logout, name='tlogout'),
    path('allnotices/', views.all_Notice, name='allnotice'),

    path('routine/create/', views.RoutineCreateView.as_view(), name='routine-create'),
    path('semester/create/', views.SemesterCreateView.as_view(), name='semester-create'),
    path('notice/create/', views.NoticeCreateView.as_view(), name='notice-create'),
#     path('notice/<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice-delete'),
    path('notice/<int:id>/delete/', views.delete_notice, name='notice-delete'),

    # path('createcmt/', views.create_Committee, name='create_committee'),
    path('view-committe-list/', views.CommitteListView.as_view(), name='viewcommittellist'),
    path('admin-page', views.AdminPageView.as_view(), name='admin_pages'),
    # 'manage-cart/<int:cp_id>'
    path('view/', views.view_semester, name='viewemny')

]
