from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientListView, ClientCreateView, ClientLoginView

router = DefaultRouter()


urlpatterns = [
    path('clients/login/', ClientLoginView.as_view(), name='client-login'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('list/', ClientListView.as_view(), name='client-list'),
    path('', include(router.urls)),
]
