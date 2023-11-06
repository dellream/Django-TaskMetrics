from django.apps import apps
from django.forms.models import modelform_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Course, Module, Content
from .forms import ModuleFormSet


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

    def dispatch(self, request, pk):
        """
        Метод предоставляется классом View.

        Определяет курс, с которым работает представление, и делегирует запрос
        соответствующему HTTP-методу.

        Args:
            request (HttpRequest): HTTP-запрос.
            pk (int): Идентификатор курса.

        Returns:
            HttpResponse: HTTP-ответ.
        """
        self.course = get_object_or_404(
            Course,
            id=pk,
            owner=self.request.user
        )
        return super().dispatch(request, pk)

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


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    Обрабатывает создание и обновление контента для модуля курса.
    """

    module = None  # Модуль, с которым связан контент
    model = None  # Модель контента
    obj = None  # Экземпляр объекта контента
    template_name = 'manage/content/form.html'

    def get_model(self, model_name):
        """
        Получает модель контента на основе переданного имени.
        """
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='education', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """
        Получает модельную форму на основе переданной модели.
        """
        form = modelform_factory(
            model,
            exclude=[
                'owner',
                'order',
                'created',
                'updated'
            ]
        )
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """
        Определяет, какой метод запроса следует использовать (GET, POST)
        и обрабатывает его.

        Аргументы:
            - module_id: ИД модуля, с которым ассоциировано/будет ассоциировано
            содержимое;
            - model_name: имя модели содержимого, которое нужно создать/обновить;
            - id: ИД обновляемого объекта. Он равен None, если создаются новые объекты.
        """
        self.module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        self.model = self.get_model(model_name)

        if id:
            self.obj = get_object_or_404(
                self.model,
                id=id,
                owner=request.user
            )

        return super().dispatch(request, module_id, model_name, id)

    # def dispatch(self, request, *args, **kwargs):
    #     self.module = get_object_or_404(
    #         Module,
    #         id=kwargs.get('module_id'),
    #         course__owner=request.user
    #     )
    #     self.model = self.get_model(kwargs.get('model_name'))
    #
    #     if kwargs.get('id'):
    #         self.obj = get_object_or_404(
    #             self.model,
    #             id=kwargs.get('id'),
    #             owner=request.user
    #         )
    #
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, module_id, model_name, id=None):
        """
        Выполняется при получении GET-запроса.

        Формируется модельная форма для обновляемого экземпляра класса контента

        Аргументы:
            - module_id: ИД модуля, с которым ассоциировано содержимое;
            - model_name: имя модели содержимого;
            - id: ИД обновляемого объекта. Он равен None, если создаются новые объекты.
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {
                'form': form,
                'object': self.obj
            }
        )

    def post(self, request, module_id, model_name, id=None):
        """
        Выполняется при получении POST-запроса.

        Обрабатывает отправку формы создания или обновления контента.

        Аргументы:
            - module_id: ИД модуля, с которым ассоциировано содержимое;
            - model_name: имя модели содержимого;
            - id: ИД обновляемого объекта. Он равен None, если создаются новые объекты.
        """
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # Создаем новый контент
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response(
            {
                'form': form,
                'object': self.obj
            }
        )


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'manage/module/content_list.html'

    def get(self, request, module_id):
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
