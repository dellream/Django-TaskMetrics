from django.shortcuts import render
from .forms import UserRegistrationForm


def user_register(request):
    """
    Регистрация пользователей
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            service_user_register(user_form)
            return render(
                request,
                'registration/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'user_form': user_form}
    )
