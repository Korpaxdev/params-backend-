from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from project.utils import serializer_validate_password
from users.models import PasswordResetTokenModel, UserModel


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    @staticmethod
    def validate_password(password: str):
        return serializer_validate_password(password)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user: UserModel = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError("Не верно введен старый пароль")
        return value

    @staticmethod
    def validate_new_password(value):
        return serializer_validate_password(value)

    def save(self, **kwargs):
        user: UserModel = self.instance
        user.set_password(self.validated_data["new_password"])
        user.save()

    class Meta:
        model = get_user_model()
        fields = ("old_password", "new_password", "id", "username", "email")
        read_only_fields = ("id", "username", "email")


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


class PasswordResetCompleteSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_password(password: str):
        return serializer_validate_password(password)

    def update(self, instance: UserModel, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id", "username", "email")
        extra_kwargs = {"password": {"write_only": True}}
