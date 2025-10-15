from datetime import timedelta, datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from booking.models import Booking


@shared_task
def send_upcoming_booking_notifications():
    now = timezone.now()
    reminder_delta = timedelta(hours=1)
    target_start = now + reminder_delta

    bookings = Booking.objects.filter(reminder_sent=False)
    for booking in bookings:
        start_dt = timezone.make_aware(
            datetime.combine(booking.date, booking.start_time),
            timezone.get_current_timezone()
        )
        if now <= start_dt <= target_start + timedelta(minutes=1):
            send_mail(
                subject=f'Напоминание о встрече: {booking.event_type.title}',
                message=f'Ваша встреча "{booking.event_type.title}" начнется в {booking.start_time}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[booking.guest.email, booking.event_type.owner.email],
                fail_silently=False,
            )
            booking.reminder_sent = True
            booking.save(update_fields=['reminder_sent'])
