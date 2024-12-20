# Generated by Django 4.2.13 on 2024-11-11 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0043_alter_producttypetypeproperty_options_and_more"),
        ("calculator", "0040_alter_valueoption_variability_with_block_amount_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="calculation",
            options={"verbose_name": "Вычисление", "verbose_name_plural": "Вычисления"},
        ),
        migrations.AddField(
            model_name="price",
            name="new_product",
            field=models.ForeignKey(
                blank=True,
                help_text="Связать с ценой товара",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="prices_in_price_lists",
                to="product.newproduct",
            ),
        ),
    ]
