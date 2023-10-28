from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView

from .models import Profile
from .services.services import service_create_user_registration_form


def user_register(request):
    """
    Регистрация пользователей
    """
    # Вызываем функцию для создания формы
    user_form, new_user = service_create_user_registration_form(request)

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


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context

# @login_required
# class ProfileEditView(UpdateView):
#     """
#     Представление для редактирования профиля
#     """
#     model = Profile
#     form_class = ProfileEditForm
#     template_name = 'account/profile/profile_edit.html'
