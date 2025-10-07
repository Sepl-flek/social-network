from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    friends = models.ManyToManyField('CustomUser', blank=True, related_name='user_friends')
    followers = models.ManyToManyField('CustomUser', blank=True, symmetrical=False, related_name='following')
    friend_requests = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='incoming_requests')

    def __str__(self):
        return self.username
