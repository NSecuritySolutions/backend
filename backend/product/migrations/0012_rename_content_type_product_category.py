# Generated by Django 4.2.11 on 2024-05-17 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0011_rename_category_product_content_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="content_type",
            new_name="category",
        ),
    ]
