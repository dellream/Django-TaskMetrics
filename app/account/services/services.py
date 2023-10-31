"""
Сервисный слой для вынесения бизнес-логики из представлений (views)
"""
from django.db import transaction
from django.urls import reverse_lazy

from ..models import Profile
from ..forms import (
    UserRegistrationForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from django.contrib import messages


def service_user_register(user_form):
    """
    Регистрация пользователя и создание для него профиля.

    :param user_form: Форма регистрации пользователя.
    :return: Объект пользователя (new_user), если форма валидна, иначе None.
    """
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        Profile.objects.create(user=new_user)
        return new_user
    return None


def service_create_user_registration_form(request):
    """
    Создание формы регистрации пользователя.

    :param request: Запрос от пользователя.
    :return: Кортеж с двумя элементами:
        - user_form: форма регистрации пользователя
        - new_user: объект нового пользователя, если регистрация прошла успешно, иначе None
    """
    if not request.method == 'POST':
        user_form = UserRegistrationForm()
    else:
        user_form = UserRegistrationForm(request.POST)
        new_user = service_user_register(user_form)
        if new_user:
            return user_form, new_user

    return user_form, None


class ServiceProfileUpdate:
    """
    Сервисный класс для вынесения логики редактирования профиля из слоя views.
    """
    @staticmethod
    def get_user_edit_form(request):
        """
        Получение формы редактирования данных пользователя.

        :param request: Запрос от пользователя.
        :return: Форма редактирования данных пользователя.
        """
        if request.POST:
            return UserUpdateForm(request.POST, instance=request.user)
        else:
            return UserUpdateForm(instance=request.user)

    @staticmethod
    def save_profile_data(request, form):
        """
        Сохранение данных профиля пользователя.

        :param request: Запрос от пользователя.
        :param form: Форма редактирования профиля.
        :return: True, если обе формы валидны и данные успешно сохранены, иначе False.
        """
        user_form = ServiceProfileUpdate.get_user_edit_form(request)
        if all([form.is_valid(), user_form.is_valid()]):
            # Следуем принципу атомарности для обязательного сохранения всех данных
            with transaction.atomic():
                user_form.save()
                form.save()
            return True
        return False

    @staticmethod
    def get_success_url(profile):
        """
        Получение URL для перенаправления после успешного редактирования профиля.

        :param profile: Профиль пользователя.
        :return: URL для перенаправления.
        """
        return reverse_lazy('profile_detail', kwargs={'slug': profile.slug})
