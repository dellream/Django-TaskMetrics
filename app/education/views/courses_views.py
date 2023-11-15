from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from education.models import Course, Subject
from account.forms import CourseEnrollForm


class OwnerMixin:
    """
    Миксин для фильтрации QuerySet'а по автору.

    Примесный класс OwnerMixin можно использовать в представлениях,
    которые взаимодействуют с любой моделью, содержащей атрибут owner.
    """

    def get_queryset(self):
        """Получает QuerySet, отфильтрованный по текущему пользователю."""
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    """
    Миксин для назначения автора объекта.
    """

    def form_valid(self, form):
        """Назначает текущего пользователя в качестве автора."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    """
    Базовый миксин для управления курсами, связанными с автором.

    Воспроизводит функциональность login_required и предоставляет
    доступ к представлению только пользователям с конкретным разрешением
    """
    model = Course
    fields = [
        'subject',
        'title',
        'slug',
        'overview'
    ]
    success_url = reverse_lazy('education:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Миксин для редактирования курсов, связанных с автором.
    """
    template_name = 'manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    Представление для отображения списка курсов автора.

    Указанное представление определяет специальный атрибут template_name для шаблона,
    который будет выводить список курсов;
    """
    template_name = 'manage/course/list.html'
    permission_required = 'education.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Представление для создания нового курса автора.

    В указанном представлении используются поля, определенные в примесном
    классе OwnerCourseMixin, чтобы компоновать модельную форму;

    Это представление также является подклассом класса CreateView.
    Оно использует шаблон, определенный в примесном классе OwnerCourseEditMixin;
    """
    permission_required = 'education.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Представление для обновления курса автора.

    Обеспечивает возможность редактировать существующий объект Course.

    В указанном представлении используются поля, определенные в примесном
    классе OwnerCourseMixin, чтобы компоновать модельную форму;

    Это представление также является подклассом класса UpdateView.
    Оно использует шаблон, определенный в примесном классе OwnerCourseEditMixin;
    """
    permission_required = 'education.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    Представление для удаления курса автора.

    В указанном представлении определяется специальный атрибут
    template_name для шаблона, который будет подтверждать удаление курса.
    """
    template_name = 'manage/course/delete.html'
    permission_required = 'education.delete_course'


class CourseListView(TemplateResponseMixin, View):
    """
    Отображает список курсов в зависимости от выбранной темы (проекта).
    """
    model = Course
    template_name = 'courses/list.html'

    def get(self, request, subject=None):
        """
        Обрабатывает GET-запрос и отображает список курсов.

        Args:
            request (HttpRequest): GET-запрос.
            subject (str): Строка со значением SLUG-а темы. По умолчанию None.

        Returns:
            HttpResponse: Ответ с отображением списка курсов.
        """
        subjects = Subject.objects.annotate(
            total_courses=Count('courses')
        )
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses
            }
        )


class CourseDetailView(DetailView):
    """
    Представление детальной информации отображения курса.

    DetailView ожидает, что pk или slug будет извлекать 1 объект курса
    """
    model = Course
    template_name = 'courses/detail.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает дополнительные данные контекста, включая форму записи на курс.

        Аргументы:
            **kwargs: Дополнительные аргументы контекста.

        Возвращает:
            dict: Словарь с данными контекста, включая форму записи на курс.
        """
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        return context
