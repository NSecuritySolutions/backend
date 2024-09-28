# Generated by Django 4.2.13 on 2024-09-28 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("calculator", "0037_alter_blockoption_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productoption",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="product_options",
                to="contenttypes.contenttype",
                verbose_name="Категория товара для фильтрации",
            ),
        ),
    ]
