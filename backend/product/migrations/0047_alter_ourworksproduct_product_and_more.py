# Generated by Django 4.2.13 on 2025-01-18 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0046_alter_newproduct_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ourworksproduct",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="ourworksproduct",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.newproduct",
            ),
        ),
        migrations.RemoveField(
            model_name="solutiontoproduct",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="solutiontoproduct",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.newproduct",
            ),
        ),
    ]
