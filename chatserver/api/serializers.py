from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from chat.models import Room, Message, Post, Comment
from account.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']


class UserSimpleSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username')


class RoomSerializer(ModelSerializer):
    owner = CustomUserSerializer()
    users = CustomUserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('name', 'owner', 'created_at', 'users')


class MessageSerializer(ModelSerializer):
    author = CustomUserSerializer()

    class Meta:
        model = Message
        fields = ('text', 'author', 'created_at')


class CommentSerializer(ModelSerializer):
    author = CustomUserSerializer()
    post_id = serializers.IntegerField(source='post.id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id','post_id', 'com', 'author', 'created_at')


class PostSerializer(ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    likes = UserSimpleSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'owner', 'image', 'likes_count', 'likes', 'comments_count', 'comments', 'created_at',)
