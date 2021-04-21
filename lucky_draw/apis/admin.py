from django.contrib import admin

from .models import Ticket, Event, EventParticipant


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    pass
