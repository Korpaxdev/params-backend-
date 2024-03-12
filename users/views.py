from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from users.models import PasswordResetTokenModel
from users.serializers import UserSerializer, PasswordResetSerializer, PasswordResetCompleteSerializer
from users.tasks import send_password_reset_email


# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer: PasswordResetSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_password_reset_email.delay(serializer.data["email"])
        return Response(serializer.data)


class ResetPasswordCompleteView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer
    queryset = PasswordResetTokenModel.objects.all()

    def get_object(self) -> PasswordResetTokenModel:
        token = self.kwargs["token"]
        return get_object_or_404(self.queryset, token=token)

    def post(self, request, *args, **kwargs):
        password_reset_token = self.get_object()
        serializer = self.serializer_class(instance=password_reset_token.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        password_reset_token.delete()
        return Response(serializer.data)
