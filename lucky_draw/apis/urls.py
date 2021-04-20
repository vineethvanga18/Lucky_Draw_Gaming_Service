from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('get-tickets', views.MyView.as_view()),
]
