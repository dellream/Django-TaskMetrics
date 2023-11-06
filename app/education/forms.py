from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module

# Создаем модельный набор форм для объектов Module, связанных с объектом Course
ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    # Поля, которые будут включены в каждую форму набора форм
    fields=[
        'title',
        'description'
    ],
    # Установим количество дополнительных пустых форм для отображения в наборе форм
    extra=2,
    # Добавим возможность удаления модуля
    can_delete=True
)
