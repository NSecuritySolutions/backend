# Generated by Django 4.2.13 on 2025-02-14 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0050_alter_solutiontoproduct_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="solutiontoproduct",
            name="show",
            field=models.BooleanField(default=True, verbose_name="Отобразить на сайте"),
        ),
    ]
