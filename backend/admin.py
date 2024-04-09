from django.contrib import admin, messages
from django.db.models import QuerySet

from backend.models import ParameterModel, BufferedParameterModel


# Register your models here.


@admin.register(ParameterModel)
class ParameterModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "cat_id", "name", "rus_name", "date", "status_delete")
    list_display_links = ("pk", "cat_id", "name")
    search_fields = ("cat_id", "name", "rus_name")
    list_filter = ("date", "status_delete")


@admin.register(BufferedParameterModel)
class BufferedParametersModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "cat_id", "name", "rus_name", "date", "status_delete", "user")
    list_display_links = ("pk", "cat_id", "name")
    search_fields = ("cat_id", "name", "rus_name", "user__username")
    list_filter = ("date", "status_delete")
    actions = ["add_params"]

    @admin.action(description="Добавить параметры в основную таблицу")
    def add_params(self, request, queryset: QuerySet[BufferedParameterModel]):
        fields = [field.name for field in ParameterModel._meta.fields if field.name not in ("id", "pk", "date")]
        params_to_table = []
        for param in queryset:
            new_param_dict = {field: getattr(param, field) for field in fields}
            params_to_table.append(ParameterModel(**new_param_dict))
        ParameterModel.objects.bulk_create(params_to_table)
        self.message_user(request, "Параметры были успешно добавлены в основную таблицу", messages.SUCCESS)
