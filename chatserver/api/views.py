from django.db.models import Q
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework import decorators
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from account.models import CustomUser
from api.serializers import (RoomSerializer, MessageSerializer, PostSerializer, CommentSerializer, UserDetailSerializer,
                             UserSimpleSerializer)
from chat.models import Room, Message, Post, Comment


# views that related with api
class RoomsViewsSet(ModelViewSet):
    queryset = Room.objects.select_related('owner').prefetch_related('users')
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyRoomListView(ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(Q(owner=user) | Q(users=user)).select_related('owner').prefetch_related(
            'users').distinct()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room__id=room_id).select_related('author')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('owner').prefetch_related('likes', 'comments__author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            return Response({'detail': 'Уже лайкнуто'}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.add(request.user)
        return Response({'detail': 'Лайк поставлен'}, status=status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        post = self.get_object()
        if request.user not in post.likes.all():
            return Response({'detail': 'Вы не ставили сюда лайк'}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.remove(request.user)
        return Response({'detail': 'Лайк убран'}, status.HTTP_204_NO_CONTENT)


class UserCommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Comment.objects.filter(Q(author=self.request.user)).select_related('author')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class UserViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().prefetch_related('friends', 'followers', 'friend_requests')
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def friends(self, request, pk=None):
        target_user = self.get_object()
        current_user = request.user

        # GET
        if request.method == 'GET':
            serializer = UserSimpleSerializer(target_user.friends.all(), many=True)
            return Response(serializer.data)

        elif request.method == 'POST':

            if target_user == current_user:
                return Response({'detail': 'Нельзя добавить в друзья самого себя'},
                                status=status.HTTP_400_BAD_REQUEST)

            if current_user in target_user.friends.all():
                return Response({'detail': 'Вы уже в друзьях'}, status=status.HTTP_400_BAD_REQUEST)

            if target_user in current_user.friend_requests.all() or target_user in current_user.followers.all():
                target_user.friends.add(current_user)
                if target_user in current_user.followers.all():
                    current_user.followers.remove(target_user)
                else:
                    current_user.friend_requests.remove(target_user)
                return Response({'detail': 'Вы добавили в друзья'}, status=status.HTTP_201_CREATED)

            else:
                return Response({'detail': 'Вы не может сделать этого'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':

            # Удалить из друзей (Переместить в подписчики)
            if current_user in target_user.friends.all():
                target_user.friends.remove(current_user)
                current_user.friends.remove(target_user)
                current_user.followers.add(target_user)
                return Response({'detail': f'Вы удалили из друзей {target_user}'}, status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def friend_request(self, request, pk=None):
        target_user = self.get_object()
        current_user = request.user

        if request.method == 'POST':
            if target_user == current_user:
                return Response({'detail': 'Нельзя кинуть заявку самому себе'},
                                status=status.HTTP_400_BAD_REQUEST)

            if target_user in current_user.friends.all():
                return Response({'detail': 'Вы уже в друзьях'},
                                status=status.HTTP_400_BAD_REQUEST)

            if current_user in target_user.followers.all() or current_user in target_user.friend_requests.all():
                target_user.followers.remove(current_user)
                return Response({'detail': 'Вы уже отправляли заявку'}, status=status.HTTP_200_OK)

            # Если пользователь уже отправлял нам заявку => мы его добавляем в друзья
            if target_user in current_user.followers.all() or target_user in current_user.friend_requests.all():
                current_user.followers.remove(target_user)
                current_user.friends.add(target_user)
                target_user.friends.add(current_user)
                return Response({'detail': 'Пользователь вам уже отправлял запрос на дружбу. Вы добавили его в друзья'},
                                status=status.HTTP_201_CREATED)
            else:
                target_user.friend_requests.add(current_user)
                return Response({'detail': f'Вы отправили заявку на дружбу {target_user}'},
                                status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if target_user == current_user:
                return Response({'detail': 'Нельзя удалить заявку себе'},
                                status=status.HTTP_400_BAD_REQUEST)

            if target_user in current_user.friends.all():
                return Response({'detail': 'Вы уже в друзьях'},
                                status=status.HTTP_400_BAD_REQUEST)

            if current_user in target_user.friend_requests.all():
                target_user.friend_requests.remove(current_user)
                return Response({'detail': 'Ваша заявка была удалена'},
                                status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'detail': 'Произошла ошибка'},
                                status=status.HTTP_400_BAD_REQUEST)
