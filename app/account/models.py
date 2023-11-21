from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


class Profile(models.Model):
    """
    Модель профиля пользователей
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    slug = models.SlugField(
        verbose_name='Слаг профиля',
        max_length=255,
        blank=True,
        unique=True
    )
    avatar = models.ImageField(
        verbose_name='Фотография профиля',
        upload_to='profile_avatars/%Y/%m/%d/',
        default='profile_avatars/default_profile_avatar.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))]
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Информация о себе'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )

    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """
        db_table = 'account_users_profiles'
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        """
        Метод сохранения профиля для создания уникального url
        для входа в профиль
        """
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Получение ссылки на профиль
        """
        return reverse('profile_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'Профиль пользователя: {self.user.username}'
