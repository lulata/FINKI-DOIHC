from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Block(models.Model):
    blocked= models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked')
    blocker= models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')

    def __str__(self):
        return self.blocked.username + ' is blocked by ' + self.blocker.username
        
class File(models.Model):
    file = models.FileField(upload_to='files/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name