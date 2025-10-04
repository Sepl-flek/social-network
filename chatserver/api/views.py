from django.db.models import Q
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import RoomSerializer, MessageSerializer, PostSerializer, CommentSerializer
from chat.models import Room, Message, Post, Comment


# views that related with api
class RoomsViewsSet(ModelViewSet):
    queryset = Room.objects.select_related('owner').prefetch_related('users')
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room__id=room_id).select_related('author')


class MyRoomListView(ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(Q(owner=user) | Q(users=user)).select_related('owner').prefetch_related(
            'users').distinct()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('owner').prefetch_related('likes', 'comments__author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserCommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Comment.objects.filter(Q(author=self.request.user)).select_related('author')
