from rest_framework.permissions import BasePermission


class AnonUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous
