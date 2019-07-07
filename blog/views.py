from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from django.utils.timezone import now
from .forms import *
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    if request.GET.get('search'):
        search = request.GET.get('search')
        news_list = News.objects.filter(
            Q(content__icontains=search) | Q(author__username__contains=search) | Q(headline__icontains=search))[::-1]
    else:
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
            comment = Comment(user=request.user,
                              text=comment_form.cleaned_data['text'],
                              news=news,
                              pub_date=now())
            Comment.save(comment)
    else:
        comment_form = CommentForm()
    news_list = News.objects.order_by('-pub_date')[:9]
    comments = Comment.objects.select_related().filter(news=blog_id)
    context = {'news': news,
               'news_list': news_list,
               'comments': comments,
               'comment_form': comment_form}
    return render(request, 'blog/news.html', context)


def blogger(request, author_username):
    try:
        UserProfile.objects.get(user__username=author_username)
    except ObjectDoesNotExist:
        return redirect('index')

    blogger_profile = UserProfile.objects.get(user__username=author_username)
    post_list = News.objects.filter(author=blogger_profile.user)
    context = {
        'blogger': blogger_profile,
        'post_list': post_list,
    }
    return render(request, 'blog/blogger.html', context)


def bloggers(request):
    bloggers_list = UserProfile.objects.all()
    context = {
        'bloggers_list': bloggers_list
    }
    return render(request, 'blog/bloggers.html', context)


def profile(request):
    try:
        UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        new_profile = UserProfile(user=request.user)
        new_profile.save()

    if request.method == 'POST' and 'bio_form' in request.POST:

        bio_form = BioForm(request.POST or None)

        if bio_form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.bio = bio_form.cleaned_data['bio']
            user_profile.save()
    else:
        bio_form = BioForm()

    if request.method == 'POST' and 'avatar_form' in request.POST:

        avatar_form = AvatarForm(request.POST, request.FILES or None)

        if avatar_form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.avatar = avatar_form.cleaned_data['avatar']
            user_profile.save()
    else:
        avatar_form = AvatarForm()

    context = {
        'bio_form': bio_form,
        'avatar_form': avatar_form,
    }
    return render(request, 'blog/profile.html', context)


def create_post(request):
    if request.method == 'POST':

        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            post = News(author=request.user,
                        content=post_form.cleaned_data['content'],
                        headline=post_form.cleaned_data['headline'],
                        image=post_form.cleaned_data['image'],
                        category=post_form.cleaned_data['category'],
                        pub_date=now())
            News.save(post)

            return redirect('index')
    else:
        post_form = PostForm()
    content = {
        'post_form': post_form,
    }
    return render(request, 'blog/create_post.html', content)
