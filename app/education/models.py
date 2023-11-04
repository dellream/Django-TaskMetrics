from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

from .service.fields import OrderField


class Subject(models.Model):
    """
    Субъект-родитель для курсов (например, может быть указан проект)
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок субъекта'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальное имя субъекта (Slug)',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Субъект-родитель курсов'
        verbose_name_plural = 'Субъекты-родители курсов'

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    Модель курса для обучения
    """
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        verbose_name='Автор курса',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
        verbose_name='Субъект-родитель'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок курса'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальное имя курса (Slug)'
    )
    overview = models.TextField(
        verbose_name='Обзор курса'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания курса'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Module(models.Model):
    """
    Модель модуля, связанная с курсом.
    """
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE,
        verbose_name='Курс для модуля'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок модуля'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание модуля'
    )
    order = OrderField(
        for_fields=['course'],
        blank=True,
        verbose_name='Порядковый номер модуля в курсе'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """
    Модель контента, связанная с модулем курса.

    Используется для хранения и отображения различных типов контента,
    таких как текстовые статьи, видеоролики, тесты и другие материалы,
    которые привязаны к конкретным модулям курса.

    Каждый объект Content связан с определенным модулем и содержит информацию
    о типе контента и объекте контента, который относится к этому модулю.
    """
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE,
        verbose_name='Модуль для текущего контента'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': (
                'text',
                'video',
                'image',
                'file'
            )
        },
        verbose_name='Тип контента'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='Идентификатор объекта контента'
    )
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(
        blank=True,
        for_fields=['module'],
        verbose_name='Порядковый номер контента в модуле'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'


class ContentBase(models.Model):
    """
    Абстрактный класс модели для контента.

    Определяет общие поля, которые будут использоваться
    во всех моделях контента при наследовании от ContentBase.
    """
    owner = models.ForeignKey(
        User,
        # динамический параметр %(class)s, который будет заменен именем класса наследника
        related_name='%(class)s_related',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ContentBase):
    content = models.TextField()


class File(ContentBase):
    file = models.FileField(upload_to='files')


class Image(ContentBase):
    file = models.FileField(upload_to='images')


class Video(ContentBase):
    url = models.URLField()
