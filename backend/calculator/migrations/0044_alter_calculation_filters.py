# Generated by Django 4.2.13 on 2024-11-11 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0043_calculation_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="calculation",
            name="filters",
            field=models.TextField(
                blank=True, null=True, verbose_name="Фильтры для товара"
            ),
        ),
    ]