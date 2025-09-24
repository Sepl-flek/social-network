from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='users')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
