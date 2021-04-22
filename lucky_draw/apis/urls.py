from django.urls import path
from . import views

urlpatterns = [
    path('get-tickets', views.GetTickets.as_view()),
    path('next-events', views.GetNextEvents.as_view()),
    path('participate', views.Participate.as_view()),
    path('list-winners', views.GetPastEventWinners.as_view()),
    path('winner', views.GetWinner.as_view()),
    path('signup', views.SignUpView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view())
]
