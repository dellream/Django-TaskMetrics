from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentaryForm, SearchForm

def home_page(request):
    return render(request, 'home.html')


def comment_list(request, tag_slug=None):
    """ Представление возвращает только опубликованные страницы, делает разбивку по страницам"""
    # Фильтруем посты на "показать только опубликованные"
    published_posts_list = Post.objects.filter(status__exact='PB')

    # Добавим определение схожести постов по тегам
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        published_posts_list = published_posts_list.filter(tags__in=[tag])

        # Создает разбивку по страницам - 3 поста на странице, минимум 2 поста на странице
    paginator = Paginator(published_posts_list, 50, orphans=2)
    page_number = request.GET.get('page', 1)
    try:
        published_posts = paginator.page(page_number)
    except EmptyPage:
        # Если page_number больше или меньше диапазона, то
        # выдать последнюю страницу
        published_posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # Если page_number не целое число, то выдать первую страницу
        published_posts = paginator.page(1)

    return render(request, 'post/list.html', {'published_posts': published_posts,
                                              'tag': tag,
                                              'section': 'comment_list'})


def comment_detail(request, year, month, day, comm):
    """
    Представление проверяет пост на наличие, возвращает 404 при отсутствии
    """
    comm = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=comm)
    # Список активных комментариев к посту
    commentaries = comm.commentary_post.filter(active=True)

    # Форма для комментирования пользователями
    form = CommentaryForm()

    # Список схожих постов
    # Извлекаем список id для тегов текущего поста; flat=True для получения [1,2,3,..], а не [(1,),(2,), ..]
    comm_tags_ids = comm.tags.values_list('id', flat=True)
    # Берем все опубликованные посты, которые содержат любой из имеющихся в списке тегов, за исключением текущего поста
    similar_comm = Post.objects.filter(status__exact='PB', tags__in=comm_tags_ids).exclude(id=comm.id)
    # Результат упорядочиваем по количеству совпадений тегов и дате публикации (сначала новые), результат режем для
    # получения первых четырех результатов
    similar_comm = similar_comm.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    # Получение списка тегов для данного поста
    tags = comm.tags.all()

    return render(request, 'post/detail.html', {'comm': comm,
                                                'commentaries': commentaries,
                                                'form': form,
                                                'tags': tags,
                                                'similar_comm': similar_comm})


def post_share(request, post_id):
    """
    Представление для отправки писем
    """
    # Извлекаем пост по идентификатору id
    post = get_object_or_404(Post,
                             pk=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    # Для отправки поста определим сценарий для POST-метода
    if request.method == 'POST':
        # Если форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Если поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} рекомендует прочитать вам {post.title}'
            message = f'Прочитайте {post.title} здесь: {post_url}\n'
            send_mail(subject, message, 'Aljoshajakimv@yandex.ru', [cd['to']])
            sent = True
            # То отправляем письмо
    # Сценарий для GET-метода
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post': post,
                                               'form': form,
                                               'sent': sent})


@require_POST
def post_commentary(request, post_id):
    """ Представление для комментирования поста """
    post = get_object_or_404(Post,
                             pk=post_id,
                             status=Post.Status.PUBLISHED)
    commentary = None
    # Отправляем комментарий
    form = CommentaryForm(data=request.POST)
    if form.is_valid():
        # Создаем объект класса Commentary, не сохраняя его в базе данных
        commentary = form.save(commit=False)
        # Назначаем пост комментарию
        commentary.post = post
        # Сохраним комментарий в БД
        commentary.save()
    return render(request, 'post/commentary.html', {'post': post,
                                                    'form': form,
                                                    'commentary': commentary})

# @require_POST
# def post_commentary(request, post_id):
#     """ Представление для комментирования поста """
#     post = get_object_or_404(Post,
#                              pk=post_id,
#                              status=Post.Status.PUBLISHED)
#     commentary = None
#     # Отправляем комментарий
#     form = CommentaryForm(data=request.POST)
#     if form.is_valid():
#         # Создаем объект класса Commentary, не сохраняя его в базе данных
#         commentary = form.save(commit=False)
#         # Назначаем пост комментарию
#         commentary.post = post
#         # Сохраним комментарий в БД
#         commentary.save()
#         # Вернуть JSON-ответ с информацией о созданном комментарии
#         return JsonResponse(
#             {
#                 'success': True,
#                 'commentary':
#                     {'id': commentary.id,
#                      'body': commentary.body,
#                      'name': commentary.name,
#                      'created': commentary.created.isoformat(),
#                      }
#             }
#         )


def post_search(request):
    """
    Представление для формы поиска
    """
    # Создадим экземпляр формы
    form = SearchForm()
    query = None
    results = []

    # Если поле в поиске пустое, то выполнить GET-запрос (не Post, чтобы можно было делиться результатом)
    if 'query' in request.GET:
        # Создаем экземпляр формы, используя переданные GET-данные
        form = SearchForm(request.GET)
        # Проверяем валидность формы
        if form.is_valid():
            # Собираем очищенные данные с поля 'query'
            query = form.cleaned_data['query']

            # search_vector = SearchVector('title', weight='A', config='russian') + \
            #                 SearchVector('body', weight='B', config='russian')
            # search_query = SearchQuery(query, config='russian')

            # Результат отфильтрован по опубликованным постам, поиску по заголовкам и телу поста
            results = Post.objects.filter(status__exact='PB') \
                .annotate(similarity=TrigramSimilarity('title', query) + TrigramSimilarity('body', query)) \
                .filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'post/search.html', {'form': form,
                                                'query': query,
                                                'results': results})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post does not exist'}, status=404)
        return JsonResponse({'status': 'error'})
