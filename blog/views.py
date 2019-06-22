from django.shortcuts import render
from .models import News


def index(request):
    news_list = News.objects.order_by('-pub_date')[:5]
    context = {
        'news_list': news_list
    }
    return render(request, 'blog/index.html', context)

