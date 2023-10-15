"""
Сервисный слой для вынесения бизнес-логики из представлений (views)
"""


def service_user_register(user_form):
    """
    Функция для регистрации пользователя
    """
    new_user = user_form.save(commit=False)
    new_user.set_password(user_form.cleaned_data['password'])
    new_user.save()

