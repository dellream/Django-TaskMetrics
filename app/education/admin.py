from django.contrib import admin
from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Subject.
    """
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    """
    Встроенная административная панель для модели Module.
    """
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Course.
    """
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
