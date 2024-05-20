# Generated by Django 4.2.11 on 2024-05-18 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0015_blockoption_product_alter_blockoption_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="calculator",
            name="formula",
        ),
        migrations.AddField(
            model_name="blockoption",
            name="filters",
            field=models.TextField(
                blank=True,
                help_text='Фильтры перечисленые через запятую, доступные операторы:\n1. Равенство: ==\n2. Неравенство: !=\n3. Больше: >\n4. Меньше: <\n5. Больше или равно: >=\n6. Меньше или равно: <=\nПример: type="HD", price<=1000',
                null=True,
                verbose_name="Фильтры для товара",
            ),
        ),
        migrations.AddField(
            model_name="calculatorblock",
            name="formula",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="calculator.formula",
            ),
        ),
        migrations.AlterField(
            model_name="blockoption",
            name="product",
            field=models.CharField(
                blank=True,
                help_text="Название категории",
                null=True,
                verbose_name="Продукт для фильтрации",
            ),
        ),
    ]