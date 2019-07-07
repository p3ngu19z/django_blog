from Django_blog.urls import path
from . import views

urlpatterns = [
    path('blog/', views.index, name='index'),
    path('', views.index, name='index'),
    path('blog/<int:blog_id>/', views.blog, name='news'),
    path('blog/blogger/<str:author_username>/', views.blogger, name='blogger'),
    path('blog/profile/', views.profile, name='profile'),
    path('blog/bloggers/', views.bloggers, name='bloggers'),
    path('blog/create/', views.create_post, name='create_post'),
]
