from django.contrib import admin

from backend.models import ParameterModel


# Register your models here.


@admin.register(ParameterModel)
class ParameterModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "cat_id", "name", "rus_name", "date", "status_delete")
    list_display_links = ("pk", "cat_id", "name")
    search_fields = ("cat_id", "name", "rus_name")
    list_filter = ("date", "status_delete")
