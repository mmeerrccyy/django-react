from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import generics
from .serializers import RoomSerializaer
from .models import Room

# Create your views here.

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializaer
