from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.admin_filters import PasswordResetTokenIsExpiredFilter
from users.models import UserModel, PasswordResetTokenModel


# Register your models here.


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(PasswordResetTokenModel)
class PasswordResetTokenModelAdmin(admin.ModelAdmin):
    readonly_fields = ("token", "created", "user", "is_expired")
    list_display = ("token", "user", "created", "is_expired")
    search_fields = ("user__username", "user__email", "token")
    list_filter = (
        PasswordResetTokenIsExpiredFilter,
        "created",
    )

    IS_EXPIRED_DISPLAYED = {True: "Да", False: "Нет"}

    @admin.display(description="Истек")
    def is_expired(self, obj):
        return self.IS_EXPIRED_DISPLAYED[obj.is_expired]
