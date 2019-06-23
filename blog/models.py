from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    class Meta:
        verbose_name_plural = "News"
    headline = models.CharField(max_length=300)
    author = models.CharField(max_length=100, default="author")
    content = RichTextUploadingField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    image = models.ImageField(upload_to="blog", default="")

    def __str__(self):
        return self.headline


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return self.username

