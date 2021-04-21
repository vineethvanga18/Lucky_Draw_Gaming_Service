from datetime import datetime, timezone, timedelta
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.renderers import JSONRenderer

from .models import User, Ticket, Event, EventParticipant
from .serializers import UserSerializer, TicketSerializer, EventSerializer


class GetTickets(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        user_id = self.request.data['user_id']
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response({
                "message": "Invalid User, No User exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            self.compute_tickets_for_user(user),
            status=status.HTTP_200_OK
        )

    def compute_tickets_for_user(self, user):
        tickets = []
        ticket_obj = Ticket(user=user)
        ticket_obj.save()
        tickets.append(
            TicketSerializer(ticket_obj).data
        )
        return tickets


class GetNextEvent(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(
            date_time__gte=datetime.now(timezone.utc)
        )


class Participate(APIView):

    def post(self, request):

        ticket = Ticket.objects.filter(
            id=self.request.data['ticket_id']
        ).first()
        event = Event.objects.filter(
            id=self.request.data['event_id']
        ).first()
        user = User.objects.filter(
            id=self.request.data['user_id']
        ).first()
        if user is None:
            return Response({
                "message": "Invalid User ID, No User Found."
            }, status=status.HTTP_400_BAD_REQUEST)

        if ticket is None or ticket.status == "CLOSED":
            return Response({
                "message": "Invalid Ticket ID, No Ticket exists."
            }, status=status.HTTP_400_BAD_REQUEST)
        if event is None or event.status == "COMPLETE":
            return Response({
                "message": "Invalid Event ID, No Event exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        if EventParticipant.objects.filter(
            user=user,
            event=event
        ).count() > 0:
            return Response({
                "message": "You are not allowed to participate twice in the same event."
            }, status=status.HTTP_400_BAD_REQUEST)

        new_participant = EventParticipant(
            user=user,
            ticket=ticket,
            event=event,
        )
        new_participant.save()
        ticket.status = "CLOSED"
        ticket.save()
        return Response({
            'Registered for Event, Successfully.'
        }, status=status.HTTP_201_CREATED)


class GetPastEventWinners(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(
            date_time__gte=datetime.now(timezone.utc) - timedelta(days=7)
        )


class GetWinner(APIView):

    def post(self, request):
        event = Event.objects.get(
            id=self.request.data['event_id']
        )
        if event is None or event.status == "COMPLETE":
            return Response({
                "message": "Invalid Event ID, No Event exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        participants = EventParticipant.objects.filter(
            event=event
        )
        if participants.count() == 0:
            return Response({
                "message": "No user participated in this event"
            }, status=status.HTTP_200_OK)

        winner = random.choice(participants)
        event.winner = User.objects.get(id=winner.user.id)
        event.status = "COMPLETE"
        event.save()

        return Response({
            "winner": UserSerializer(event.winner).data
        }, status=status.HTTP_200_OK)
