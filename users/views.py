from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http.request import validate_host
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlencode
from requests import Session
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from users.models import PasswordResetTokenModel, UserModel
from users.serializers import (
    UserSerializer,
    PasswordResetSerializer,
    PasswordResetCompleteSerializer,
    PasswordChangeSerializer,
)
from users.tasks import send_password_reset_email


# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfilePasswordChangeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer: PasswordResetSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_password_reset_email.delay(serializer.validated_data["email"], serializer.validated_data.get("next"))
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


class OauthCompleteView(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    url_validator = URLValidator()

    def get(self, request: Request, *args, **kwargs):
        redirect_url = self.build_redirect_url()
        redirect_response = redirect("parameters")
        if redirect_url:
            token_params = self.get_tokens(request.user)
            redirect_response = redirect(redirect_url + f"?{token_params}")
        logout(request)
        return redirect_response

    def build_redirect_url(self):
        session: Session = self.request.session
        next_url = str(session.get("next"))
        scheme = self.get_validated_scheme(str(session.get("scheme")))
        return self.get_redirect_url(next_url, scheme)

    def get_redirect_url(self, next_url, scheme):
        scheme = str(scheme) if scheme else "http"
        try:
            redirect_url = f"{scheme}://{next_url}"
            self.url_validator(redirect_url)
            netlog = urlparse(redirect_url).netloc
            if validate_host(netlog, settings.ALLOWED_HOSTS):
                return redirect_url
        except ValidationError:
            return None

    @staticmethod
    def get_tokens(user: UserModel):
        tokens = {"refresh": RefreshToken.for_user(user), "access": AccessToken.for_user(user)}
        return urlencode(tokens)

    @staticmethod
    def get_validated_scheme(value: str):
        if value in ["http", "https"]:
            return value
        return "http"
