# Generated by Django 4.2.13 on 2024-11-12 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0010_rename_is_active_ourguarantees_active_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reviews",
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
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                ("title", models.CharField(max_length=100, verbose_name="Заголовок")),
                ("text", models.TextField(max_length=2000, verbose_name="Текст")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/reviews",
                        verbose_name="Аватарка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddField(
            model_name="employee",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="ourguarantees",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="ourguarantees",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="questions",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="questionscategory",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="questionscategory",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="socialinfo",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="socialinfo",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="subguarantees",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="subguarantees",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата обновления"
            ),
        ),
    ]