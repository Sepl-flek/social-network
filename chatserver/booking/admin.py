from django.contrib import admin

from booking.models import Booking, EventType, Availability


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    pass
