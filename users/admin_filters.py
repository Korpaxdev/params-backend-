from django.contrib import admin


class PasswordResetTokenIsExpiredFilter(admin.SimpleListFilter):
    title = "Истек"
    parameter_name = "is_expired"

    def lookups(self, request, model_admin):
        return [
            (True, "Да"),
            (False, "Нет"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        mapper = {"False": False, "True": True}
        if not value:
            return queryset
        value = mapper[self.value()]
        ids = map(lambda model: model.pk, filter(lambda model: model.is_expired == value, queryset))
        return queryset.filter(id__in=ids)
