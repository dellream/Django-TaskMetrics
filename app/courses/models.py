from django.db import models
from django.contrib.auth.models import User


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
    Модель модулей курсов.
    Каждый курс поделен на модули.
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

    class Meta:
        ordering = ['title']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.title


