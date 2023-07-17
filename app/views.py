from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .mixins import ClientMixin
from .models import Client
from .permissions import AnonUserPermission
from .serializers import ClientSerializer, ClientPostSerializer, ClientLoginSerializer


class ClientViewSet(ClientMixin):
    queryset = Client.objects.all()
    # serializer_class = ClientSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientPostSerializer
        return ClientSerializer

    def get_permissions(self):
        print('*'*30, self.action)
        if self.action in ('list', 'create'):
            return [permissions.AllowAny()]
        return super(self, ClientViewSet).get_permissions()

    # @action(methods=['POST'],
    #         detail=False,
    #         permission_classes=[permissions.AllowAny])
    def create(self, request):

        return Response({'data': 'created'}, status=status.HTTP_201_CREATED)


class ClientLoginView(APIView):
    permission_classes = [AnonUserPermission]

    def post(self, request):
        data = ClientLoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = authenticate(**data.validated_data)
        try:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            return Response(
                {
                    'refresh': str(refresh_token),
                    'access': str(access_token)
                },
                status=status.HTTP_201_CREATED,
            )
        except AttributeError:
            return Response(
                {'detail': 'Такого пользователя не существует'},
                status=status.HTTP_404_NOT_FOUND,
            )


class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientPostSerializer
    permission_classes = [permissions.AllowAny]


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]
