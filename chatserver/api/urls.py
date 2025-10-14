from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import RoomsViewsSet, MessageListView, MyRoomListView, PostViewSet, UserViewSet, PostFeedViewSet, \
    CommunityViewSet

router = SimpleRouter()
router.register(r'rooms', RoomsViewsSet)
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
router.register(r'feed', PostFeedViewSet, basename='feed-post')
router.register(r'communities', CommunityViewSet)

urlpatterns = [path('rooms/<int:room_id>/messages/',  MessageListView.as_view(), name='room-message'),
               path('rooms/user_room/', MyRoomListView.as_view(), name='user-rooms')]

urlpatterns += router.urls
