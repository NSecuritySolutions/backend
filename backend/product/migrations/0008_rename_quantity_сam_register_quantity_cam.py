# Generated by Django 4.2.11 on 2024-05-09 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0007_register_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="register",
            old_name="quantity_сam",
            new_name="quantity_cam",
        ),
    ]
