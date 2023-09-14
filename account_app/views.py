from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return False


class UserListCreateRetrieveUpdateDestroyAPIViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == 'list' and not self.request.user.is_superuser:
            return [IsAdminUser()]
        elif self.action == 'create':
            return []
        return super().get_permissions()
