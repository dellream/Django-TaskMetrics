from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('', views.home_page, name='home'),
    # Статьи
    path('comments/', views.comment_list, name='comment_list'),
    # Детализация поста
    path('<int:year>/<int:month>/<int:day>/<slug:comm>/',
         views.comment_detail,
         name='comment_detail'),
    # Поделиться записью
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # Создать комментарий
    path('<int:post_id>/commentary/',
         views.post_commentary, name='post_commentary'),
    # Отображение списка постов по тегу
    path('tag/<slug:tag_slug>/',
         views.comment_list, name='comment_list_by_tag'),
    path('search/', views.post_search, name='post_search'),
    path('like/', views.post_like, name='like'),
]
