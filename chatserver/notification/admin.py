from django.contrib import admin
from django.contrib.admin import ModelAdmin

from notification.models import Notification


@admin.register(Notification)
class NotificationsAdmin(ModelAdmin):
    pass
