# Generated by Django 5.0.1 on 2024-02-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0005_alter_camera_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='domestic',
            field=models.IntegerField(default=0, verbose_name='Внутренние'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='external',
            field=models.IntegerField(default=0, verbose_name='Внешние'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='quality',
            field=models.CharField(choices=[('HD', 'HD'), ('FullHD', 'FullHD'), ('2K-4K', '2K-4K')], max_length=6, verbose_name='Качество изображения'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='system_type',
            field=models.CharField(choices=[('AHD', 'AHD'), ('IP', 'IP')], max_length=4, verbose_name='Тип системы'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='time',
            field=models.CharField(choices=[('7', '7'), ('14', '14'), ('30', '30')], max_length=5, verbose_name='Время хранение видео'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='total_price',
            field=models.IntegerField(verbose_name='Итог'),
        ),
    ]