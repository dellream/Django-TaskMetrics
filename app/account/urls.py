from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # Регистрация пользователя
    path('register/', views.user_register, name='register'),

    # Просмотр профиля
    path('profile/<str:slug>/',
         views.ProfileDetailView.as_view(),
         name='profile_detail'),

    # Редактирование профиля
    path('profile/<str:slug>/edit',
         views.ProfileUpdateView.as_view(),
         name='profile_edit'),

    # Взаимодействие с курсами
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/',
         views.StudentCourseListView.as_view(),
         name='student_course_list'),
    path('course/<pk>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
]
