# Generated by Django 4.2.13 on 2024-06-01 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0018_pricelist_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pricelist",
            name="is_current",
        ),
    ]