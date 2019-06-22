from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News


def index(request):
    news_list = News.objects.all()[::-1]
    paginator = Paginator(news_list, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    context = {
        'news_list': news,
    }

    return render(request, 'blog/index.html', context)

