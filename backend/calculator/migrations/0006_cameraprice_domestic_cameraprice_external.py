# Generated by Django 5.0.1 on 2024-02-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0005_cameraprice"),
    ]

    operations = [
        migrations.AddField(
            model_name="cameraprice",
            name="domestic",
            field=models.IntegerField(default=0, verbose_name="Внутренние"),
        ),
        migrations.AddField(
            model_name="cameraprice",
            name="external",
            field=models.IntegerField(default=0, verbose_name="Внешние"),
        ),
    ]
