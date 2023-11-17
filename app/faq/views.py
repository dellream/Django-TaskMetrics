from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

from .models import Post
from .forms import CommentaryForm


def faq_list(request):
    """ Представление возвращает только опубликованные страницы, делает разбивку по страницам"""
    # Фильтруем посты на "показать только опубликованные"
    published_posts_list = Post.objects.filter(status__exact='PB')

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

    return render(request,
                  'post/list.html',
                  {
                      'published_posts': published_posts,
                      'section': 'comment_list'}
                  )


def faq_detail(request, year, month, day, comm):
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

    return render(
        request,
        'post/detail.html',
        {
            'comm': comm,
            'commentaries': commentaries,
            'form': form
        }
    )


@require_POST
def faq_commentary(request, post_id):
    """ Представление для комментирования поста """
    post = get_object_or_404(
        Post,
        pk=post_id,
        status=Post.Status.PUBLISHED
    )

    if request.method == 'POST':
        form = CommentaryForm(data=request.POST, request=request)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.post = post  # Установим связанный пост для комментария
            commentary.save()
            return redirect('faq:faq_list')
    else:
        form = CommentaryForm(request=request)

    return render(
        request,
        'post/commentary.html',
        {
            'post': post,
            'form': form,
        }
    )
