# Generated by Django 5.0.1 on 2024-02-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Camera",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "time",
                    models.CharField(
                        choices=[("7", "7"), ("14", "14"), ("30", "30")],
                        max_length=5,
                        verbose_name="Время хранение видео",
                    ),
                ),
                (
                    "system_type",
                    models.CharField(
                        choices=[("AHD", "AHD"), ("IP", "IP")],
                        max_length=4,
                        verbose_name="Тип системы",
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        choices=[
                            ("HD", "HD"),
                            ("FullHD", "FullHD"),
                            ("2K-4K", "2K-4K"),
                        ],
                        max_length=6,
                        verbose_name="Качество изображения",
                    ),
                ),
                ("external", models.IntegerField(default=0, verbose_name="Внешние")),
                ("domestic", models.IntegerField(default=0, verbose_name="Внутренние")),
                ("total_price", models.IntegerField(verbose_name="Итог")),
                ("name", models.CharField(max_length=20, verbose_name="ФИО")),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="Почта"),
                ),
                ("number", models.IntegerField(verbose_name="Номер телефона")),
            ],
            options={
                "verbose_name": "Конфигурации камер",
                "verbose_name_plural": "Конфигурации камер",
            },
        ),
    ]
