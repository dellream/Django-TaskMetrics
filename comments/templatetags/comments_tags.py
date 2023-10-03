from django import template
from ..models import Post

# Переменная register - экземпляр template.Library(), регистрирует шаблонные теги и фильтры приложения
register = template.Library()


@register.inclusion_tag('post/latest_post.html')
def show_latest_posts(count: int = 4) -> dict[str, any]:
    """
    Возвращает словарь переменных (последние опубликованные посты)
    """
    latest_posts = Post.objects.filter(status__exact='PB').order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
