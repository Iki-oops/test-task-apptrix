from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .mixins import ClientMixin
from .models import Client
from .serializers import ClientSerializer, ClientPostSerializer


class ClientViewSet(ClientMixin):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(methods=['POST'],
            detail=False,
            permission_classes=[permissions.AllowAny])
    def create(self, request):

        return Response({'data': 'created'}, status=status.HTTP_201_CREATED)


class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientPostSerializer
    permission_classes = [permissions.AllowAny]


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]
