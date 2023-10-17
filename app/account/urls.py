from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [

    # Вход и выход
    path('login/',
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             authentication_form=LoginForm
         ),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logged_out'),

    # Смена пароля
    path('password-change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Сброс пароля
    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # Встроенные представления аутентификации
    # path('', include('django.contrib.auth.urls')),

    # Работа с пользователями
    # Регистрация пользователя
    path('register/', views.user_register, name='register'),
    # Редактирование пользователя
    path('edit/', views.edit_user_and_profile, name='edit_user_and_profile'),
]
