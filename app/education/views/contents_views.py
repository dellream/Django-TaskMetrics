from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from django.apps import apps
from django.forms.models import modelform_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View

from education.models import Course, Module, Content
from education.forms import ModuleFormSet


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
            return redirect('education:module_content_list', self.module.id)
        return self.render_to_response(
            {
                'form': form,
                'object': self.obj
            }
        )


class ContentDeleteView(View):
    """
    Удаляет содержимое (контент) модуля.
    """

    def post(self, request, id):
        """
        Обрабатывает POST-запрос для удаления содержимого модуля.

        Args:
            request (HttpRequest): HTTP-запрос.
            id (int): Идентификатор содержимого для удаления.

        Returns:
            HttpResponseRedirect: После успешного удаления перенаправляет на список содержимого модуля.
        """
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('education:module_content_list', module.id)


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    """
    Представление для обновления порядка следования контента модулей
    """

    def post(self, request):
        for content_id, order in self.request_json.items():
            Content.objects.filter(
                id=content_id,
                module__course__owner=request.user
            ).update(order=order)

        return self.render_json_response(
            {
                'saved': 'OK'
            }
        )
