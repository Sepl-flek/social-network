from rest_framework.serializers import ModelSerializer
from chat.models import Room
from account.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']


class RoomSerializer(ModelSerializer):
    owner = CustomUserSerializer()
    users = CustomUserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('name', 'owner', 'created_at', 'users')
