from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from education.models import Course
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
        delete_avatar = form.cleaned_data.get('delete_avatar')
        if delete_avatar:
            profile = self.get_object()
            profile.avatar.delete()

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
        self.course.students.add(self.request.user)
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


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
    Представление списка курсов для студента.

    Attributes:
        model (Course): Модель курса.
        template_name (str): Имя шаблона для отображения списка курсов.

    Methods:
        get_queryset(): Получает и возвращает queryset курсов для текущего студента.
    """
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        """
        Получает и возвращает queryset курсов для текущего студента.

        Returns:
            QuerySet: queryset курсов для текущего студента.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """
    Представление детальной информации о курсе для студента.

    Attributes:
        model (Course): Модель курса.
        template_name (str): Имя шаблона для отображения детальной информации.

    Methods:
        get_queryset(): Получает и возвращает queryset курсов для текущего студента.
        get_context_data(**kwargs): Получает и возвращает контекст для отображения детальной информации о курсе.
    """
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        """
        Получает и возвращает queryset курсов для текущего студента.

        Returns:
            QuerySet: queryset курсов для текущего студента.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        """
        Получает и возвращает контекст для отображения детальной информации о курсе.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Контекст для отображения детальной информации о курсе.
        """
        context = super().get_context_data(**kwargs)

        # Получить объект Course
        course = self.get_object()

        if 'module_id' in self.kwargs:
            # Взять текущий модуль
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # Взять первый модуль
            context['module'] = course.modules.all()[0]

        return context


if __name__ == '__main__':
    # Интроспекция класса UpdateView
    from django.views.generic import UpdateView

    methods_of_update_view = list(method for method in dir(UpdateView) if not method.startswith('__'))
    for method_name in methods_of_update_view:
        method = getattr(UpdateView, method_name)  # Получить объект метода
        docstring = method.__doc__  # Получить документацию метода
        if docstring:
            print(f"Method: {method_name}\nDocumentation: {docstring}\n")
