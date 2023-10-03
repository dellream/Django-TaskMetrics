from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager

from config import settings


class Post(models.Model):
    """ Модель для информации о постах """

    class Status(models.TextChoices):
        """ Определение вариантов статусов """
        DRAFT = 'DT', 'Черновик'
        PUBLISHED = 'PB', 'Опубликовано'

    # Добавим менеджер тегов, который позволит добав., удал., извлекать теги из объектов Post
    tags = TaggableManager()

    # Добавление автора в качестве внешнего ключа
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments_user')
    title = models.CharField(max_length=100)  # Заголовок поста

    # Уникальный идентификатор поста (необходим для создания URL)
    slug = models.SlugField(max_length=30,
                            unique_for_date='publish')
    body = models.TextField()  # Текстовое содержимое поста
    publish = models.DateTimeField(default=timezone.now)  # Дата и время публикации поста
    created = models.DateTimeField(auto_now_add=True)  # Дата и время создания поста
    updated = models.DateTimeField(auto_now=True)  # Дата и время последнего обновления поста
    deleted = models.DateTimeField(auto_now_add=True)  # Дата и время последнего удаления поста
    status = models.CharField(max_length=2,
                              default=Status.DRAFT,
                              choices=Status.choices)
    users_like = models.ManyToManyField(User,
                                        related_name='posts_liked',
                                        blank=True)

    class Meta:
        """ Дополнительные настройки модели Post """
        ordering = ['-publish']  # Определяет порядок сортировки постов по атрибуту publish
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comments:comment_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Commentary(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='commentary_post')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.name} оставил комментарий под постом {self.post}'

