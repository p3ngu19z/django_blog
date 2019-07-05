from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import News, Comment, UserProfile
from django.utils.timezone import now
from .forms import CommentForm, BioForm, AvatarForm
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


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


def blogger(request, author_username):
    try:
        UserProfile.objects.get(user__username=author_username)
    except ObjectDoesNotExist:
        return redirect('index')

    blogger_profile = UserProfile.objects.get(user__username=author_username)
    context = {
        'blogger': blogger_profile,
    }
    return render(request, 'blog/blogger.html', context)


def bloggers(request):
    return render(request, 'blog/bloggers.html')


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
