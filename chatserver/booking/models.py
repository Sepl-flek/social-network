from django.conf import settings
from django.db import models


class EventType(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_events')
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    location = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title} ({self.duration_minutes} мин)"


class Availability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="availability")
    weekday = models.IntegerField(choices=[(i, day) for i, day in enumerate(
        ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    )])
    start_time = models.TimeField()
    end_time = models.TimeField()


class Booking(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="bookings")
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hosted_bookings")

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("host", "date", "start_time")

    def __str__(self):
        return f"{self.guest_name} → {self.host} ({self.date} {self.start_time})"
