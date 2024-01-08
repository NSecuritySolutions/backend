# Generated by Django 5.0.1 on 2024-01-08 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Материал')),
            ],
            options={
                'verbose_name': 'Модели',
                'verbose_name_plural': 'Модели',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=30, verbose_name='Модель')),
                ('descriptoin', models.TextField(max_length=500, verbose_name='Описание')),
                ('resolution', models.CharField(max_length=20, verbose_name='Разрешение')),
                ('material', models.ManyToManyField(to='product.material', verbose_name='Материал')),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
