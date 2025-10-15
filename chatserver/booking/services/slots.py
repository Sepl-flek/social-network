from datetime import datetime, timedelta
from booking.models import Availability, Booking


def get_available_slots(event_type, date, duration_minutes):
    """
    Возвращает список доступных временных слотов для пользователя в указанный день.
    """
    user = event_type.owner
    weekday = date.weekday()
    availabilities = Availability.objects.filter(user=user, weekday=weekday)

    # Брони за день
    existing_bookings = Booking.objects.filter(event_type=event_type, date=date)
    booked_intervals = [(b.start_time, b.end_time) for b in existing_bookings]

    free_slots = []
    delta = timedelta(minutes=duration_minutes)

    for avail in availabilities:
        start = datetime.combine(date, avail.start_time)
        end = datetime.combine(date, avail.end_time)

        current = start
        while current + delta <= end:
            slot_start = current.time()
            slot_end = (current + delta).time()

            conflict = any(
                slot_start < b_end and slot_end > b_start
                for b_start, b_end in booked_intervals
            )

            if not conflict:
                free_slots.append((slot_start, slot_end))

            current += delta

    return free_slots
