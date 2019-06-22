from Django_blog.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:news_id>/', views.news, name='news')
]


