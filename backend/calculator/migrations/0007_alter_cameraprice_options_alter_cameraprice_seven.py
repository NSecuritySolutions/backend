# Generated by Django 5.0.1 on 2024-02-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0006_cameraprice_domestic_cameraprice_external"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cameraprice",
            options={
                "verbose_name": "Цены на камеры",
                "verbose_name_plural": "Цены на камеры",
            },
        ),
        migrations.AlterField(
            model_name="cameraprice",
            name="seven",
            field=models.IntegerField(verbose_name="Внешние"),
        ),
    ]
