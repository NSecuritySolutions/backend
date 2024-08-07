# Generated by Django 4.2.13 on 2024-07-29 17:50

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0029_alter_readysolution_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HDD",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="product.product",
                    ),
                ),
                (
                    "capacity",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Ёмкость, tb",
                    ),
                ),
            ],
            options={
                "verbose_name": "Жёсткий диск",
                "verbose_name_plural": "Жёсткие диски",
            },
            bases=("product.product",),
        ),
    ]
