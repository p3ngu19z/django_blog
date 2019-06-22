from django.db import models


class News(models.Model):
    class Meta:
        verbose_name_plural = "News"
    headline = models.CharField(max_length=300)
    author = models.CharField(max_length=100, default="author")
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(upload_to="blog", default="")

    def __str__(self):
        return self.headline

