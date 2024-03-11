from rest_framework import generics, permissions
from rest_framework.response import Response

from users.serializers import UserSerializer, PasswordResetSerializer


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
        return Response(serializer.data)
