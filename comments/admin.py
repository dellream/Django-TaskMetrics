from django.contrib import admin
from .models import Post, Commentary

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Класс для адаптации внешнего вида модели Post """
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # Корректировка отображения полей
    list_filter = ['status', 'created', 'publish', 'author']  # Отображение фильтров
    search_fields = ['title', 'body']  # Создание строки поиска
    prepopulated_fields = {'slug': ('title',)}  # Предзаполнение поля 'slug' в зависимости от заголовка
    raw_id_fields = ['author']  # Отображение виджета для отбора ассоциированных объектов модели Post
    date_hierarchy = 'publish'  # Навигация в фильтре по иерархии дат
    ordering = ['status', 'publish']  # Сортировка постов по столбцам 'status' и 'publish'

@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'email', 'post', 'created']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
