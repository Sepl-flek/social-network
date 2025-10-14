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
    community = models.ForeignKey('Community', on_delete=models.CASCADE,
                                  related_name='posts', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True)

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)


class Community(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_communities')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_communities',
                                     through='CommunityMembership', blank=True)

    image = models.ImageField(upload_to='uploads/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def members_count(self):
        return self.members.count()

    def __str__(self):
        return self.name


class CommunityMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20,
        choices=[
            ('member', 'Участник'),
            ('admin', 'Администратор'),
            ('moderator', 'Модератор'),
        ],
        default='member'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')

    def __str__(self):
        return f"{self.user.username} в {self.community.name} ({self.role})"
