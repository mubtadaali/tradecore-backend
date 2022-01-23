from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.viewsets import ModelViewSet

from apps.services.exceptions import EmailValidationTimeoutException
from apps.users.constants import EMAIL_TIME_OUT_MSG
from apps.users.serializers import SignUpSerializer, UpdatePasswordSerializer, UserSerializer
from apps.users.permissions import IsAdminOrIsSelf


class UserViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions for user
    """
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (IsAuthenticated, )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    queryset = User.objects.filter(is_active=True)
    ordering_fields = ['id', 'username', 'email']
    ordering = ['-id']

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == ['update', 'partial_update', 'update_password']:
            permission_classes = [IsAdminOrIsSelf]
        elif self.action == ['destroy']:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        elif self.action == 'update_password':
            return UpdatePasswordSerializer

        return UserSerializer

    @action(detail=True, methods=['patch'])
    def update_password(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except EmailValidationTimeoutException:
            return Response(EMAIL_TIME_OUT_MSG, status=HTTP_503_SERVICE_UNAVAILABLE)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])
