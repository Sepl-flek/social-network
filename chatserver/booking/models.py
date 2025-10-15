from datetime import datetime, timedelta

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
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guested_bookings")

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ("guest", "date", "start_time")

    def save(self, *args, **kwargs):
        if self.start_time and not self.end_time and self.event_type:
            dt = datetime.combine(self.date, self.start_time)
            dt_end = dt + timedelta(minutes=self.event_type.duration_minutes)
            self.end_time = dt_end.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest.username} → {self.event_type.owner.username} ({self.date} {self.start_time})"
