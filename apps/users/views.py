from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_504_GATEWAY_TIMEOUT
from rest_framework.views import APIView

from apps.services.exceptions import EmailValidationTimeoutException
from apps.users.constants import EMAIL_TIME_OUT_MSG
from apps.users.serializers import SignInSerializer, SignUpSerializer, UpdatePasswordSerializer
from apps.users.permissions import IsUnAuthenticated, IsUserThemselves


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except EmailValidationTimeoutException:
            return Response(EMAIL_TIME_OUT_MSG, status=HTTP_504_GATEWAY_TIMEOUT)


class SignInView(APIView):
    permission_classes = (IsUnAuthenticated, )

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=HTTP_200_OK)


class SignOutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response('User Logged out successfully', status=HTTP_200_OK)


class UpdatePassword(UpdateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UpdatePasswordSerializer
    permission_classes = (IsAuthenticated, IsUserThemselves)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response('Password Updated Successfully!', status=HTTP_200_OK)
