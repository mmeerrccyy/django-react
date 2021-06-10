from django.db.models import query
from django.http.request import host_validation_re
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import generics, serializers, status
from .serializers import RoomSerializaer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializaer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = room.code
                return Response(RoomSerializaer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializaer(room).data, status=status.HTTP_201_CREATED)


class GetRoomView(APIView):
    serializer_class = RoomSerializaer
    lookup_url_kwarg = 'code'

    def get(self, request, *args, **kwargs):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            if Room.objects.filter(code=code).exists():
                room = Room.objects.filter(code=code)
                data = RoomSerializaer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoomView(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            roomResult = Room.objects.filter(code=code)
            if len(roomResult) > 0:
                room = roomResult[0]
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Room Code!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Room With This Code Does Not Exists!'}, status=status.HTTP_404_NOT_FOUND)


class UserInRoomView(APIView):

    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoomView(APIView):

    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            code = self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_result = Room.objects.filter(host=host_id)
            if len(room_result) > 0:
                room = room_result[0]
                room.delete()

        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)