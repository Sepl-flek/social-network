from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import RoomsViewsSet, MessageListView

router = SimpleRouter()
router.register(r'rooms', RoomsViewsSet)

urlpatterns = [path('rooms/<int:room_id>/messages/',  MessageListView.as_view(), name='room-message')]

urlpatterns += router.urls
