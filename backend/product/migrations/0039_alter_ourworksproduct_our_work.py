# Generated by Django 4.2.13 on 2024-10-12 04:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0038_productcategory_level_productcategory_lft_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ourworksproduct",
            name="our_work",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="product.ourworks",
            ),
        ),
    ]
