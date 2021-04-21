from django.urls import path
from . import views

urlpatterns = [
    path('get-tickets/<int:user_id>', views.GetTickets.as_view()),
    path('next-events', views.GetNextEvent.as_view()),
    path('participate', views.Participate.as_view()),
    path('list-winners', views.GetPastEventWinners.as_view()),
    path('winner', views.GetWinner.as_view()),
]
