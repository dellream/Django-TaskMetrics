from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Профиль пользователей в админке
    """
    list_display = [
        'user',
        'slug',
        'avatar',
        'bio',
        'birth_date',
    ]
