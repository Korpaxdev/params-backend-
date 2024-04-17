from django.contrib import admin


class PasswordResetTokenIsExpiredFilter(admin.SimpleListFilter):
    """Фильтр для истечения срока действия токена для сброса пароля"""

    title = "Истек"
    parameter_name = "is_expired"

    def lookups(self, request, model_admin):
        return [
            (True, "Да"),
            (False, "Нет"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        if isinstance(value, str):
            mapper = {"True": True, "False": False}
            value = mapper[value]
        ids = map(lambda model: model.pk, filter(lambda model: model.is_expired == value, queryset))
        return queryset.filter(id__in=ids)
