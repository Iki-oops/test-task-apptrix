import django_filters
from django.db.models.expressions import RawSQL

from .models import Client


class ClientFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='istartswith')
    last_name = django_filters.CharFilter(lookup_expr='istartswith')
    max_distance = django_filters.NumberFilter(method='filter_max_distance')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'sex', 'max_distance']

    def filter_max_distance(self, queryset, name, value):
        is_anonymous = self.request.user.is_anonymous

        if value != 'false' and value != '0' and not is_anonymous:
            longitude, latitude = self.request.user.longitude, self.request.user.latitude
            gcd_formula = ("6371 * acos(cos(radians(%s)) * "
                           "cos(radians(latitude)) * cos(radians(longitude) - "
                           "radians(%s)) + sin(radians(%s)) * sin(radians(latitude)))")
            distance_raw_sql = RawSQL(
                gcd_formula,
                (latitude, longitude, latitude)
            )
            queryset = queryset.annotate(distance=distance_raw_sql)
            return queryset.filter(distance__lte=int(value))
        return queryset
