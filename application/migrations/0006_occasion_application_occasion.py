# Generated by Django 5.0.1 on 2024-02-06 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_alter_application_description_alter_application_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Повод заявки')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='occasion',
            field=models.ManyToManyField(default='Обычная Заявка', to='application.occasion', verbose_name='Повод заявки'),
        ),
    ]
