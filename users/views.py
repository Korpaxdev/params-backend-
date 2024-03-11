from rest_framework import generics, permissions

from users.serializers import UserSerializer


# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
