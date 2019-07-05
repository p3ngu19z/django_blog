from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News, Comment
from django.utils.timezone import now
from .forms import CommentForm
from django.http import HttpResponse


def index(request):
    news_list = News.objects.all()[::-1]
    paginator = Paginator(news_list, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    context = {
        'news_list': news,
    }

    return render(request, 'blog/index.html', context)


def blog(request, blog_id):
    news = News.objects.get(id=blog_id)
    if request.method == 'POST':

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = Comment(username=comment_form.cleaned_data['username'],
                              text=comment_form.cleaned_data['text'],
                              news=news,
                              email=comment_form.cleaned_data['email'],
                              pub_date=now())
            Comment.save(comment)

            return HttpResponse("Спасибо за комментарий")
    else:
        comment_form = CommentForm()
    news_list = News.objects.order_by('-pub_date')[:9]
    comments = Comment.objects.select_related().filter(news=blog_id)
    context = {'news': news,
               'news_list': news_list,
               'comments': comments,
               'comment_form': comment_form}
    return render(request, 'blog/post.html', context)


def blogger(request, author_id):
    pass


def bloggers(request):
    return render(request, 'blog/bloggers.html')
