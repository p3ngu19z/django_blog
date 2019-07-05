from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=600, default='There should be your biography')
    avatar = models.ImageField(upload_to='avatars', default='avatars/user.png')

    def __str__(self):
        return self.user.username


class News(models.Model):
    class Meta:
        verbose_name_plural = "News"
    headline = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, default='other')
    content = RichTextUploadingField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    image = models.ImageField(upload_to="blog", default="")

    def get_comments_count(self):
        return Comment.objects.filter(news=self.id).count()

    def __str__(self):
        return self.headline


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()
    email = models.EmailField(default='')

    def __str__(self):
        return "{username} - {text}".format(username=self.username, text=self.text[:75])

