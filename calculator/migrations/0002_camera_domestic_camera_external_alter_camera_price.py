# Generated by Django 5.0.1 on 2024-02-06 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='domestic',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='camera',
            name='external',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='camera',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=1000),
        ),
    ]
