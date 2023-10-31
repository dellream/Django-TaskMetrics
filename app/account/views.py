from django.db import transaction
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile
from .services.services import service_create_user_registration_form, ServiceProfileUpdate


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


# class ProfileEditView(UpdateView):
#     """
#     Представление для редактирования профиля
#     """
#     model = Profile
#     form_class = ProfileEditForm
#     template_name = 'profile/profile_edit.html'
#
#     def get_object(self, queryset=None):
#         return self.request.user.profile
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
#         context['user_form'] = ServiceProfileEdit.get_user_edit_form(self.request)
#         return context
#
#     def form_valid(self, form):
#         if ServiceProfileEdit.save_profile_data(self.request, form):
#             return super(ProfileEditView, self).form_valid(form)
#         else:
#             context = self.get_context_data()
#             return self.render_to_response(context)
#
#     def get_success_url(self):
#         return ServiceProfileEdit.get_success_url(self.object)

class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})



if __name__ == '__main__':
    # Интроспекция класса UpdateView
    from django.views.generic import UpdateView

    methods_of_update_view = list(method for method in dir(UpdateView) if not method.startswith('__'))
    for method_name in methods_of_update_view:
        method = getattr(UpdateView, method_name)  # Получить объект метода
        docstring = method.__doc__  # Получить документацию метода
        if docstring:
            print(f"Method: {method_name}\nDocumentation: {docstring}\n")
