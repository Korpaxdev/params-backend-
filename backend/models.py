from django.db import models


# Create your models here.


class ParameterModel(models.Model):
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
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"
