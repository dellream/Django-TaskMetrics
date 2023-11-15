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

    # Зачисление на курс
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
]
