from django.db import models

from users.models import UserModel


# Create your models here.
class ParameterAbstractModel(models.Model):
    """Абстрактная (для наследования другими моделями) модель параметров"""

    cat_id = models.CharField(max_length=4, verbose_name="Идентификатор пакета CAN шины")
    data_length = models.CharField(max_length=50, verbose_name="Длинна")
    length = models.CharField(max_length=50, verbose_name="Длина занимаемая значением")
    name = models.CharField(max_length=100, verbose_name="Наименование")
    rus_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование на русском")
    scaling = models.CharField(max_length=100, verbose_name="Коэффициент")
    range = models.CharField(max_length=100, verbose_name="Диапазон")
    spn = models.IntegerField(verbose_name="SPN")
    date = models.DateTimeField(auto_now=True, verbose_name="Дата записи")
    status_delete = models.BooleanField(default=False, verbose_name="Статус удаления")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ParameterModel(ParameterAbstractModel):
    """Модель для представления параметров"""

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"
        ordering = ["id"]


class BufferedParameterModel(ParameterAbstractModel):
    """Модель для представления параметров созданных пользователем"""

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name="Пользователь")
    sync_with_main_table = models.BooleanField(
        default=False, auto_created=True, verbose_name="Синхронизировано с основной таблицей"
    )

    class Meta:
        verbose_name = "Параметр пользователя"
        verbose_name_plural = "Параметры пользователей"


class SyncLoggingModel(models.Model):
    """Модель для логирования пользовательских действий с параметрами"""

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now=True, verbose_name="Дата синхронизации")
    params_marked_to_delete = models.ManyToManyField(ParameterModel, verbose_name="Параметры помеченные на удаление")
    new_params = models.ManyToManyField(BufferedParameterModel, verbose_name="Параметры добавленные пользователем")

    def __str__(self):
        return f"Логер #{self.pk}"

    class Meta:
        verbose_name = "Логер синхронизации"
        verbose_name_plural = "Логеры синхронизации"
