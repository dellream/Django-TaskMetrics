from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileUpdateForm, CourseEnrollForm
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
        context['user_form'] = ServiceProfileUpdate.get_user_edit_form(self.request)
        return context

    def form_valid(self, form):
        if ServiceProfileUpdate.save_profile_data(self.request, form):
            return super(ProfileUpdateView, self).form_valid(form)
        else:
            context = self.get_context_data()
            return self.render_to_response(context)

    def get_success_url(self):
        return ServiceProfileUpdate.get_success_url(self.object)


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    Представление для обработки запросов на запись студента на курс.

    Атрибуты:
        course (Course): Курс, на который записывается студент.
        form_class (class): Класс формы, используемый для записи.

    Методы:
        form_valid(form): Обрабатывает случай, когда форма является валидной, и записывает студента на курс.
        get_success_url(): Возвращает URL для перенаправления после успешной записи.
    """
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        """
        Обрабатывает случай, когда форма является валидной, и записывает студента на курс.

        Аргументы:
            form (CourseEnrollForm): Валидная форма записи.

        Возвращает:
            HttpResponse: Перенаправляет на URL успешной записи.
        """
        self.course = form.cleaned_data['course']
        self.course.account.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешной записи.

        Возвращает:
            str: URL успешной записи.
        """
        return reverse_lazy(
            'account:student_course_detail',
            args=[self.course.id]
        )


if __name__ == '__main__':
    # Интроспекция класса UpdateView
    from django.views.generic import UpdateView

    methods_of_update_view = list(method for method in dir(UpdateView) if not method.startswith('__'))
    for method_name in methods_of_update_view:
        method = getattr(UpdateView, method_name)  # Получить объект метода
        docstring = method.__doc__  # Получить документацию метода
        if docstring:
            print(f"Method: {method_name}\nDocumentation: {docstring}\n")
