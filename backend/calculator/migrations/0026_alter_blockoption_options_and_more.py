# Generated by Django 4.2.13 on 2024-07-10 21:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0025_alter_blockoption_option_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blockoption",
            options={
                "ordering": ("position",),
                "verbose_name": "Опция для блока",
                "verbose_name_plural": "Опции блока",
            },
        ),
        migrations.AlterModelOptions(
            name="calculatorblock",
            options={
                "ordering": ("position",),
                "verbose_name": "Блок калькулятора",
                "verbose_name_plural": "Блоки калькулятора",
            },
        ),
        migrations.AddField(
            model_name="blockoption",
            name="position",
            field=models.IntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Позиция в списке",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="calculatorblock",
            name="position",
            field=models.IntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Позиция в списке",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="formula",
            name="expression",
            field=models.TextField(
                help_text="Синтаксис math.js + функции:\n1. if(условие, значение при истино, значение при ложно)\n2. str_equals(строка, строка)",
                verbose_name="Формула",
            ),
        ),
    ]
