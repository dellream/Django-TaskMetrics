from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View

from education.models import Course, Module, Content
from education.forms import ModuleFormSet


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    Представление для управления модулями в рамках курса.
    Для редактирования модулей использует формы ModuleFormSet.

    Attributes:
        template_name (str): Имя шаблона, который будет использоваться для отображения формы.
        course (Course): Курс, с которым работает представление.

    Method:
        get_formset(data=None): Создает и возвращает форму ModuleFormSet для заданного курса.
    """
    template_name = 'manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """
        Создает и возвращает форму ModuleFormSet для заданного курса.

        Args:
            data: Данные для инициализации формы. По умолчанию None.

        Returns:
            ModuleFormSet: Форма для модулей, связанных с курсом.
        """
        return ModuleFormSet(
            instance=self.course,
            data=data
        )

    def dispatch(self, request, course_id):
        """
        Метод предоставляется классом View.

        Определяет курс, с которым работает представление, и делегирует запрос
        соответствующему HTTP-методу.

        Args:
            request (HttpRequest): HTTP-запрос.
            course_id (int): Идентификатор курса.

        Returns:
            HttpResponse: HTTP-ответ.
        """
        self.course = get_object_or_404(
            Course,
            id=course_id,
            owner=self.request.user
        )
        return super().dispatch(request, course_id)

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос и отображает форму для редактирования модулей.

        Args:
            request (HttpRequest): GET-запрос.

        Returns:
            HttpResponse: HTTP-ответ с отображением формы для редактирования модулей.
        """
        formset = self.get_formset()
        return self.render_to_response(
            {
                'course': self.course,
                'formset': formset
            }
        )

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос и сохраняет изменения модулей.

        Args:
            request (HttpRequest): POST-запрос.

        Returns:
            HttpResponse: После успешного сохранения, перенаправляет на список курсов.
        """
        formset = self.get_formset(data=request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('education:manage_course_list')
        return self.render_to_response(
            {
                'course': self.course,
                'formset': formset
            }
        )


class ModuleContentListView(TemplateResponseMixin, View):
    """
    Отображает список содержимого модуля.
    """
    template_name = 'manage/module/content_list.html'

    def get(self, request, module_id):
        """
        Обрабатывает GET-запрос и отображает список содержимого модуля.

        Args:
            request (HttpRequest): GET-запрос.
            module_id (int): Идентификатор модуля, содержимое которого необходимо отобразить.

        Returns:
            HttpResponse: Ответ с отображением списка содержимого модуля.
        """
        module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        return self.render_to_response(
            {
                'module': module
            }
        )


class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    """
    Представление для обновления порядка следования модулей курса
    """

    def post(self, request):
        for module_id, order in self.request_json.items():
            Module.objects.filter(
                id=module_id,
                course__owner=request.user
            ).update(order=order)
        return self.render_json_response(
            {
                'saved': 'OK'
            }
        )
