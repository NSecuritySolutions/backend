# Generated by Django 5.0.1 on 2024-02-09 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0007_alter_cameraprice_options_alter_cameraprice_seven"),
    ]

    operations = [
        migrations.AlterField(
            model_name="camera",
            name="total_price",
            field=models.FloatField(
                blank=True, default=0, null=True, verbose_name="Итог"
            ),
        ),
    ]
