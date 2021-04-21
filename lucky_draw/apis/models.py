from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = (
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    )
    status = models.CharField(choices=status_choices, max_length=10, default="ACTIVE")

    def __str__(self):
        return "RaffleTicket- {}".format(self.id)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Event(models.Model):
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

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-date_time']


class EventParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.event)
