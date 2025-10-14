from django.contrib import admin
from django.contrib.admin import ModelAdmin

from chat.models import Room, Message, Post, Comment, Community, CommunityMembership


@admin.register(Room)
class RoomsAdmin(ModelAdmin):
    pass


@admin.register(Message)
class MessagesAdmin(ModelAdmin):
    pass


@admin.register(Post)
class PostsAdmin(ModelAdmin):
    pass


@admin.register(Comment)
class CommentsAdmin(ModelAdmin):
    pass


@admin.register(Community)
class CommunityAdmin(ModelAdmin):
    pass


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(ModelAdmin):
    pass
