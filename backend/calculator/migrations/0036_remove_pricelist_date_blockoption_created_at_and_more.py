# Generated by Django 4.2.13 on 2024-09-28 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0035_blockoption_initial_value_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pricelist",
            name="date",
        ),
        migrations.AddField(
            model_name="blockoption",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="blockoption",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="calculator",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="calculator",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="calculatorblock",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="calculatorblock",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="formula",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="formula",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="price",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="price",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="pricelist",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="pricelist",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="pricelistcategory",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="pricelistcategory",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
    ]
