from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {"password": {"write_only": True}}
