from django.db import models

# Create your models here.
class Post(models.Model):
    content    = models.TextField()
    created_at = models.DateTimeField()
    def __str__(self):
        return self.content

class Comment(models.Model):
    comment    = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment