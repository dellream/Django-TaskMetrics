"""
Сервисный слой для вынесения бизнес-логики из представлений (views)
"""
from ..models import Profile
from ..forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from django.contrib import messages


def service_user_register(user_form):
    """
    Регистрация пользователя и создание для него профиля
    Возвращает new_user, если форма валидна, иначе None
    """
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        Profile.objects.create(user=new_user)
        return new_user
    return None


def service_create_user_registration_from(request):
    """
    Создание формы регистрации
    Возвращает форму регистрации пользователя и new_user,
    если пользователь новый, если существующий, то
    возвращает форму и None
    """
    if not request.method == 'POST':
        user_form = UserRegistrationForm()
    else:
        user_form = UserRegistrationForm(request.POST)
        new_user = service_user_register(user_form)
        if new_user:
            return user_form, new_user

    return user_form, None


def service_edit_user_and_profile(request):
    """
    Редактирование пользователя и его профиля
    """
    if not request.method == 'POST':
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    else:
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Профиль успешно изменен')
        else:
            messages.error(request, 'Ошибка изменения профиля')

    return user_form, profile_form
