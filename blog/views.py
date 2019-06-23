from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News, Comment
from django.utils.timezone import now


def index(request):
    news_list = News.objects.all()[::-1]
    paginator = Paginator(news_list, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    context = {
        'news_list': news,
    }

    return render(request, 'blog/index.html', context)


def news(request, news_id):
    news = News.objects.get(id=news_id)
    if request.method == 'POST':
        comment = Comment(username=request.POST.get('username'),
                          text=request.POST.get('text'),
                          news=news,
                          pub_date=now())
        Comment.save(comment)
    news_list = News.objects.order_by('-pub_date')[:9]
    comments = Comment.objects.select_related().filter(news=news_id)
    return render(request, 'blog/news.html', {'news': news, 'news_list': news_list, 'comments': comments})
