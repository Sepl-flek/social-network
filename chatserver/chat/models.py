from django.db import models
from django.conf import settings


class Room(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='liked_posts',
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    com = models.CharField(max_length=512)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
