# Generated by Django 4.2.13 on 2024-11-11 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0044_alter_productproperty_options_alter_newproduct_model_and_more",
        ),
        ("calculator", "0042_remove_calculation_product_remove_price_product_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculation",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.producttype",
                verbose_name="Вид товара",
            ),
        ),
    ]