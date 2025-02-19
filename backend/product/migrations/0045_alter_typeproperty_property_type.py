# Generated by Django 4.2.13 on 2024-11-11 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0044_alter_productproperty_options_alter_newproduct_model_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="typeproperty",
            name="property_type",
            field=models.CharField(
                choices=[
                    ("text", "Текст"),
                    ("integer", "Целое число"),
                    ("float", "Десятичное число"),
                    ("boolean", "Логический тип"),
                ],
                default="text",
                max_length=10,
                verbose_name="Тип характеристики",
            ),
        ),
    ]
