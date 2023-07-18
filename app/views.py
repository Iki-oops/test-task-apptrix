from smtplib import SMTPDataError

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import ClientFilter
from .mixins import ClientMixin
from .models import Client, Match
from .permissions import AnonUserPermission
from .serializers import ClientSerializer, ClientPostSerializer, ClientLoginSerializer
from .utils import add_watermark, send_mail_to_clients


class ClientViewSet(ClientMixin):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(methods=['POST'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def match(self, request, pk=None):
        initiator = request.user
        confirmer = get_object_or_404(Client, pk=pk)

        if initiator == confirmer:
            return Response(
                {'detail': 'Вы не можете выбрать самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            match = Match.objects.get(
                Q(initiator=initiator, confirmer=confirmer) |
                Q(initiator=confirmer, confirmer=initiator)
            )

            if match.is_accepted or match.is_declined:
                return Response(
                    {'detail': 'Вы уже отвечали на этот мэтч'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif match.initiator == initiator:
                return Response(
                    {'detail': 'Вы уже отправляли мэтч этому пользователю'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif match.initiator == confirmer:
                match.is_accepted = True
                match.save()

                try:
                    clients = [
                        {
                            'name': initiator.get_full_name(),
                            'email': initiator.email,
                            'email_to': confirmer.email
                        },
                        {
                            'name': confirmer.get_full_name(),
                            'email': confirmer.email,
                            'email_to': initiator.email
                        },
                    ]
                    send_mail_to_clients(clients)
                except SMTPDataError:
                    return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

                return Response(
                    {'data': {'email': initiator.email}},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {'detail': 'Что-то пошло не так'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except ObjectDoesNotExist:
            Match.objects.create(
                initiator=initiator,
                confirmer=confirmer,
            )
            return Response(
                {'detail': 'Мэтч создан'},
                status=status.HTTP_201_CREATED,
            )


class ClientLoginView(APIView):
    permission_classes = (AnonUserPermission,)

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
    permission_classes = (AnonUserPermission,)

    def perform_create(self, serializer):
        serializer.save()
        add_watermark(
            serializer.validated_data.get('avatar').name
        )


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClientFilter
