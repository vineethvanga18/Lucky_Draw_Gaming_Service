from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    """
    A simple Model for Tickets. A ticket is created when requested.
    A ticket is associated with a single user. A user can have multiple tickets.
    It has a status field which states if it is used or not
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = (
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    )
    status = models.CharField(choices=status_choices, max_length=10, default="ACTIVE")

    def __str__(self):
        return "RaffleTicket- {}".format(self.id)

    def set_status(self, new):
        self.status = new
        self.save()

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Event(models.Model):
    """
    A Model for Events. Each event has a title, date, time,
    prize, winner.It also has a status field to indicate if that event
    is completed or not
    """
    title = models.CharField(max_length=64)
    date_time = models.DateTimeField()
    prize = models.CharField(max_length=64)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status_choices = (
        ('ACTIVE', 'Active'),
        ('COMPLETE', 'Complete'),
    )
    status = models.CharField(choices=status_choices, max_length=10, default="ACTIVE")

    def __str__(self):
        return self.title

    def set_status(self, new):
        self.status = new
        self.save()

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class EventParticipant(models.Model):
    """
    A Model for an Event Participant.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.event)
