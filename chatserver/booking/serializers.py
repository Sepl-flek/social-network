from rest_framework import serializers

from api.serializers import UserSimpleSerializer
from .models import Booking, EventType


class EventTypeSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)

    class Meta:
        model = EventType
        fields = ('title', 'owner', 'description', 'duration_minutes', 'location', 'slug')


class BookingSerializer(serializers.ModelSerializer):
    event_type = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())
    guest = UserSimpleSerializer(read_only=True)
    #event_type_pk = serializers.IntegerField(source='event_type_pk')

    class Meta:
        model = Booking
        fields = ('event_type', 'guest', 'date', 'start_time', 'end_time', 'created_at')

    def validate(self, data):
        guest = self.context['request'].user
        date = data['date']
        start = data['start_time']
        end = data['end_time']

        conflict = Booking.objects.filter(
            guest=guest,
            date=date,
            start_time__lt=end,
            end_time__gt=start
        ).exists()

        if conflict:
            raise serializers.ValidationError("Этот слот уже занят")

        return data
