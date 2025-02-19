# Generated by Django 4.2.13 on 2025-02-14 23:41

from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0051_solutiontoproduct_show"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newproduct",
            options={"verbose_name": "Товар", "verbose_name_plural": "Товары"},
        ),
        migrations.AlterModelOptions(
            name="ourworksproduct",
            options={
                "verbose_name": "Использованный товар",
                "verbose_name_plural": "Использованные товары",
            },
        ),
        migrations.AlterField(
            model_name="ourworks",
            name="budget",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Бюджет",
            ),
        ),
    ]
