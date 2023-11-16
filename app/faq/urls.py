from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    # Статьи
    path('comments/', views.faq_list, name='comment_list'),

    # Детализация поста
    path('<int:year>/<int:month>/<int:day>/<slug:comm>/',
         views.faq_detail,
         name='comment_detail'),

    # Создать комментарий
    path('<int:post_id>/commentary/',
         views.faq_commentary, name='post_commentary')
]
