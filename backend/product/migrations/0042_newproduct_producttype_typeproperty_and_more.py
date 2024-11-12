# Generated by Django 4.2.13 on 2024-11-11 13:56

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import product.validators


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0041_register_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата обновления"
                    ),
                ),
                (
                    "article",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Артикул"
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        help_text="Название поля: model",
                        max_length=300,
                        verbose_name="Модель",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/product",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=5000, verbose_name="Описание"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0"),
                        help_text="Название поля: price",
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0"))
                        ],
                        verbose_name="Цена",
                    ),
                ),
                (
                    "tooltip",
                    models.TextField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Информация в тултипе",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.productcategory",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.manufacturer",
                        verbose_name="Производитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата обновления"
                    ),
                ),
                ("name", models.CharField(verbose_name="Название")),
            ],
            options={
                "verbose_name": "Вид товара",
                "verbose_name_plural": "Виды товаров",
            },
        ),
        migrations.CreateModel(
            name="TypeProperty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата обновления"
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        validators=[product.validators.validate_field_name],
                        verbose_name="Название поля характеристики",
                    ),
                ),
                ("name", models.CharField(verbose_name="Название характеристики")),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("integer", "Integer"),
                            ("float", "Float"),
                            ("boolean", "Boolean"),
                        ],
                        default="text",
                        max_length=10,
                        verbose_name="Тип характеристики",
                    ),
                ),
            ],
            options={
                "verbose_name": "Хар-ка вида товара",
                "verbose_name_plural": "Хар-ки видов товаров",
            },
        ),
        migrations.CreateModel(
            name="ProductTypeTypeProperty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата обновления"
                    ),
                ),
                (
                    "producttype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.producttype",
                    ),
                ),
                (
                    "typeproperty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.typeproperty",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="producttype",
            name="properties",
            field=models.ManyToManyField(
                related_name="product_types",
                through="product.ProductTypeTypeProperty",
                to="product.typeproperty",
            ),
        ),
        migrations.CreateModel(
            name="ProductProperty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата обновления"
                    ),
                ),
                ("value", models.CharField(blank=True, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to="product.newproduct",
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.typeproperty",
                    ),
                ),
            ],
            options={
                "verbose_name": "Хар-ка товара",
                "verbose_name_plural": "Хар-ки товаров",
            },
        ),
        migrations.AddField(
            model_name="newproduct",
            name="product_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="product.producttype",
            ),
        ),
    ]