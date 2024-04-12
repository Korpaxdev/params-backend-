from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from backend.models import ParameterModel, BufferedParameterModel, SyncLoggingModel


# Register your models here.


class SyncLoggingParamsTabularInline(admin.TabularInline):
    model = SyncLoggingModel.params_marked_to_delete.through
    verbose_name = "Параметр помеченный на удаление"
    verbose_name_plural = "Параметры помеченные на удаление"
    extra = 1
    raw_id_fields = ("parametermodel",)


class SyncLoggingNewParamsTabularInline(admin.TabularInline):
    model = SyncLoggingModel.new_params.through
    verbose_name = "Параметр добавленный пользователем"
    verbose_name_plural = "Параметры добавленные пользователем"
    extra = 1
    raw_id_fields = ("bufferedparametermodel",)


@admin.register(ParameterModel)
class ParameterModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "cat_id", "name", "rus_name", "date", "status_delete")
    list_display_links = ("pk", "cat_id", "name")
    search_fields = ("cat_id", "name", "rus_name")
    list_filter = ("date", "status_delete")
    actions = ("unmark_to_delete", "mark_to_delete")

    @admin.action(description="Снять с удаления")
    def unmark_to_delete(self, request: HttpRequest, queryset: QuerySet[ParameterModel]):
        queryset.update(status_delete=False)

    @admin.action(description="Пометить на удаление")
    def mark_to_delete(self, request: HttpRequest, queryset: QuerySet[ParameterModel]):
        queryset.update(status_delete=True)


@admin.register(BufferedParameterModel)
class BufferedParametersModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "cat_id", "name", "rus_name", "date", "status_delete", "user", "sync_with_main_table")
    list_display_links = ("pk", "cat_id", "name")
    search_fields = ("cat_id", "name", "rus_name", "user__username")
    list_filter = ("date", "status_delete")
    readonly_fields = ("sync_with_main_table",)
    actions = ["add_params"]

    @admin.action(description="Добавить параметры в основную таблицу")
    def add_params(self, request, queryset: QuerySet[BufferedParameterModel]):
        fields = [field.name for field in ParameterModel._meta.fields if field.name not in ("id", "pk", "date")]
        params_to_table = []
        no_sync_params = []
        synced_params = []
        for param in queryset:
            if param.sync_with_main_table:
                no_sync_params.append(param)
                continue
            new_param_dict = {field: getattr(param, field) for field in fields}
            params_to_table.append(ParameterModel(**new_param_dict))
            param.sync_with_main_table = True
            param.save()
            synced_params.append(param)
        ParameterModel.objects.bulk_create(params_to_table)

        if synced_params:
            params_to_table_ids_str = ",".join([str(param.pk) for param in synced_params])
            self.message_user(
                request,
                f"Параметры с id - {params_to_table_ids_str} были успешно добавлены в основную таблицу",
                messages.SUCCESS,
            )
        if no_sync_params:
            params_no_sync_ids_str = ",".join([str(param.pk) for param in no_sync_params])
            self.message_user(
                request,
                f"Параметры с id - {params_no_sync_ids_str} не были добавлены в основную таблицу. "
                f"Так как уже до этого были синхронизированы с ней",
                messages.WARNING,
            )


@admin.register(SyncLoggingModel)
class SyncLoggingAdmin(admin.ModelAdmin):
    inlines = (SyncLoggingParamsTabularInline, SyncLoggingNewParamsTabularInline)
    list_display = ("pk", "user", "date", "count_of_marked_to_delete", "count_of_new_params")
    fields = ("user", "date")
    readonly_fields = ("date",)
    list_display_links = ("pk", "user")

    @admin.display(description="Количество параметров на удаление")
    def count_of_marked_to_delete(self, instance: SyncLoggingModel):
        return instance.params_marked_to_delete.count()

    @admin.display(description="Количество новых параметров")
    def count_of_new_params(self, instance: SyncLoggingModel):
        return instance.new_params.count()
