from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


class ClientMixin(RetrieveModelMixin, GenericViewSet):
    pass
