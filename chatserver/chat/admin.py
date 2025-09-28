from django.contrib import admin
from django.contrib.admin import ModelAdmin

from chat.models import Room, Message


@admin.register(Room)
class RoomsAdmin(ModelAdmin):
    pass


@admin.register(Message)
class MessagesAdmin(ModelAdmin):
    pass
