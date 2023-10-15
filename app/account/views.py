from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from app.account.forms import LoginForm


def user_login(request):
    """
    Представление входа пользователя в систему
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Если данные введены правильно, считываем данные
        if not form.is_valid():
            form = LoginForm()
        else:
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

            # Проверка, существует ли пользователь
            if user is None:
                return HttpResponse('Неправильный логин или пароль')
            else:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Аутентификация прошла успешно')
                else:
                    return HttpResponse('Отключенная учетная запись')

        return render(
            request,
            'account/login.html',
            {'form': form}
        )
