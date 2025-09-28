from rest_framework.serializers import ModelSerializer

from chat.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'owner', 'created_at')