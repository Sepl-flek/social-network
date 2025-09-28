from django.contrib import admin
from django.contrib.admin import ModelAdmin

from account.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class MessagesAdmin(ModelAdmin):
    pass
