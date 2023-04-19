from django.urls import path,re_path
from .views import *
from rest_framework import permissions



urlpatterns = [

    path('', Partida.as_view()),
]