from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import PasswordResetTokenModel


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    @staticmethod
    def validate_password(password: str):
        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(detail=error.messages)
        return password

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField(read_only=True, default=settings.DEFAULT_PASSWORD_RESET_MESSAGE)

    def save(self):
        email = self.validated_data["email"]
        try:
            user = get_user_model().objects.get(email=email)
            old_token = PasswordResetTokenModel.objects.filter(user=user).first()
            if old_token:
                old_token.delete()
            return PasswordResetTokenModel.objects.create(user=user)
        except get_user_model().DoesNotExist:
            return
