# Generated by Django 5.0.1 on 2024-01-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_date_finis_ourworks_date_finish'),
    ]

    operations = [
        migrations.AddField(
            model_name='ourworks',
            name='product',
            field=models.ManyToManyField(to='product.product', verbose_name='Используемое оборудование'),
        ),
    ]