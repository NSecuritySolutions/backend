# Generated by Django 4.2.13 on 2024-10-26 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0005_remove_calculatorblockdata_calculator_data_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
    ]
