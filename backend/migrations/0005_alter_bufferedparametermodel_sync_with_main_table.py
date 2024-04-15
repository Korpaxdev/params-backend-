# Generated by Django 5.0.3 on 2024-04-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0004_bufferedparametermodel_sync_with_main_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bufferedparametermodel",
            name="sync_with_main_table",
            field=models.BooleanField(
                auto_created=True, default=False, verbose_name="Синхронизировано с основной таблицей"
            ),
        ),
    ]
