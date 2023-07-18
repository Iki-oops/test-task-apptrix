import django_filters

from .models import Client


class ClientFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='istartswith')
    last_name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'sex']
