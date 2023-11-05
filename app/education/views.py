from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course



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
    success_url = reverse_lazy('manage_course_list')


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
