# Generated by Django 4.2.13 on 2025-02-16 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0050_calculatorblock_main_product_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PriceList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата обновления"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="media/price_list", verbose_name="Файл с прайс листом"
                    ),
                ),
            ],
            options={
                "verbose_name": "Прайс лист",
                "verbose_name_plural": "Прайс листы",
            },
        ),
        migrations.RemoveField(
            model_name="calculatorblock",
            name="formula",
        ),
        migrations.AlterField(
            model_name="calculation",
            name="amount",
            field=models.TextField(
                help_text="Значение или формула для вычисления значения. Синтаксис math.js + функции:\n1. if(условие, значение при истино, значение при ложно)\n2. str_equals(строка, строка)",
                verbose_name="Кол-во",
            ),
        ),
        migrations.DeleteModel(
            name="Formula",
        ),
        migrations.AddField(
            model_name="calculator",
            name="price_list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="calculator.pricelist",
            ),
        ),
    ]
