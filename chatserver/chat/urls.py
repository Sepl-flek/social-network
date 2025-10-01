from django.urls import path
from rest_framework.routers import SimpleRouter

from chat.views import index, room


urlpatterns = [
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room")
]
