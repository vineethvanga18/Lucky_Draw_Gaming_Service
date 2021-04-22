from datetime import datetime, timezone, timedelta
import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.renderers import JSONRenderer

from .models import User, Ticket, Event, EventParticipant
from .serializers import UserSerializer, TicketSerializer, EventSerializer, FutureEventSerializer
from .forms import NewUserForm


class GetTickets(APIView):
    """
    API which allows users to get the raffle tickets.
    Returns a single ticket on every request for a particular user
    """
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """
        A Get method which returns a ticket for an Authenticated User.

        :param request
        :return Response Object with Ticket details
        """
        user = self.request.user
        if not user.is_authenticated:
            return Response({
                "message": "Invalid User, No User exists."
            }, status=status.HTTP_401_UNAUTHORIZED)
        ticket = Ticket(user=user)
        ticket.save()
        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_200_OK
        )


class GetNextEvents(generics.ListAPIView):
    """
    Returns Upcoming Lucky Draw Events timing & the corresponding reward.
    """
    renderer_classes = [JSONRenderer]
    serializer_class = FutureEventSerializer

    def get_queryset(self):
        return Event.objects.filter(
            date_time__gte=datetime.now(timezone.utc)
        ).order_by('date_time')


class Participate(APIView):
    """
    API which allows users to participate in a game.
    """
    def post(self, request):
        """
        A Post method for participating in an event for an Authenticated User.

        :param request:
        :return Response Object with a message
        """
        user = self.request.user
        if not user.is_authenticated:
            return Response({
                "message": "Invalid User, No User exists."
            }, status=status.HTTP_401_UNAUTHORIZED)

        ticket = Ticket.objects.filter(
            id=self.request.data['ticket_id'],
        ).first()

        event = Event.objects.filter(
            id=self.request.data['event_id']
        ).first()

        if ticket is None or ticket.status == "CLOSED" or ticket.user.id is not user.id:
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
        ticket.set_status("CLOSED")
        return Response({
            "message": "Registered for Event, Successfully."
        }, status=status.HTTP_201_CREATED)


class GetPastEventWinners(generics.ListAPIView):
    """
    Returns all the winners of all the events in the last one week.
    """
    renderer_classes = [JSONRenderer]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(
            date_time__gte=datetime.now(timezone.utc) - timedelta(days=7),
            date_time__lte=datetime.now(timezone.utc)
        ).order_by('-date_time')


class GetWinner(APIView):
    """
    API for Computing and Announcing the winner for an event.
    """
    def post(self, request):
        """
        A Post method which computes winner randomly for an Event

        :param request:
        :return Response Object with winner details
        """
        event = Event.objects.get(
            id=self.request.data['event_id']
        )

        if event is None or event.status == "COMPLETE":
            return Response({
                "message": "Invalid Event ID, No Event exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        participants = EventParticipant.objects.filter(event=event)
        if participants.count() == 0:
            return Response({
                "message": "No user participated in this event"
            }, status=status.HTTP_200_OK)

        winner = random.choice(participants)
        event.winner = User.objects.get(id=winner.user.id)
        event.set_status("COMPLETE")

        return Response({
            "winner": UserSerializer(event.winner).data
        }, status=status.HTTP_200_OK)


class SignUpView(APIView):
    """
    API for User Registration
    """
    def post(self, request):
        """
        A Post method to validate the credentials and register the user

        :param request:
        :return: Response Object with User details
        """
        form = NewUserForm(self.request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response({
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Unsuccessful registration. Invalid information."
            }, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    API for User Login
    """
    def post(self, request):
        """
        A Post method to validate the credentials and authenticate the User

        :param request:
        :return: Response Object with User details
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({
                    "user": UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Invalid username or password."
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid username or password."
            }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API for User Logout
    """
    def get(self, request):
        """

        :param request:
        :return: Response Object with a message
        """
        logout(request)
        return Response({
            "message": "User successfully logged out"
        }, status=status.HTTP_200_OK)
