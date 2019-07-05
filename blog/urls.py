from Django_blog.urls import path
from . import views

urlpatterns = [
    path('blog/', views.index, name='index'),
    path('', views.index, name='index'),
    path('blog/<int:blog_id>/', views.blog, name='news'),
    path('blog/blogeer/<int:author_id>/', views.blogger, name='blogger'),
    path('blog/bloggers/', views.bloggers, name='bloggers'),
    # path('blog/<int:blog-id>/create/'),
]
