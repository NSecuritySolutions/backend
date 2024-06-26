# Generated by Django 5.0.1 on 2024-02-08 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
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
                "verbose_name": "Заявки",
                "verbose_name_plural": "Заявки",
            },
        ),
    ]
