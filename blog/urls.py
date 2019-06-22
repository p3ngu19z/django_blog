from Django_blog.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]


