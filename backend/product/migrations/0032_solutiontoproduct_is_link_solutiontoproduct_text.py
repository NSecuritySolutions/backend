# Generated by Django 4.2.13 on 2024-08-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0031_alter_hdd_capacity"),
    ]

    operations = [
        migrations.AddField(
            model_name="solutiontoproduct",
            name="is_link",
            field=models.BooleanField(
                default=False,
                help_text="Отобразить как ссылку на товар",
                verbose_name="Ссылка",
            ),
        ),
        migrations.AddField(
            model_name="solutiontoproduct",
            name="text",
            field=models.CharField(
                default="",
                help_text="Краткое описание",
                max_length=200,
                verbose_name="Текст",
            ),
            preserve_default=False,
        ),
    ]
