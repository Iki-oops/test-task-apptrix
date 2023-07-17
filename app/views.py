from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Client
from .permissions import AnonUserPermission
from .serializers import ClientSerializer, ClientPostSerializer, ClientLoginSerializer
from .utils import add_watermark


class ClientLoginView(APIView):
    permission_classes = [AnonUserPermission]

    def post(self, request):
        serializer = ClientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = get_object_or_404(
            Client,
            email=serializer.validated_data.get('email')
        )

        check_password = client.check_password(serializer.validated_data.get('password'))

        if not check_password:
            return Response(
                data={'message': 'Пароль не совпадает'},
                status=status.HTTP_400_BAD_REQUEST)

        refresh_token = RefreshToken.for_user(client)
        access_token = refresh_token.access_token
        return Response(
            {
                'refresh': str(refresh_token),
                'access': str(access_token)
            },
            status=status.HTTP_201_CREATED,
        )


class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientPostSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        add_watermark(
            serializer.validated_data.get('avatar').name
        )


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]
