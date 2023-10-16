from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .services.services import (
    service_user_register,
    service_edit_user_and_profile,
    service_create_user_registration_from,
)


def user_register(request):
    """
    Регистрация пользователей
    """
    # Вызываем функцию для создания формы
    user_form, new_user = service_create_user_registration_from(request)

    # Если создаем нового пользователя:
    if new_user:
        return render(
            request,
            'registration/register_done.html',
            {'new_user': new_user}
        )

    # Если создаваемый пользователь уже существует:
    return render(
        request,
        'registration/register.html',
        {'user_form': user_form}
    )


@login_required
def edit_user_and_profile(request):
    """
    Редактирование пользователя и его профиля
    """
    user_form, profile_form = service_edit_user_and_profile(request)

    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )
