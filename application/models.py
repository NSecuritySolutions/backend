from django.db import models

# Create your models here.

class Application(models.Model):
    name = models.CharField(verbose_name='ФИО',max_length=40)
    email = models.EmailField(verbose_name='Почта')
    company = models.CharField(verbose_name='Компания',max_length=20)
    number = models.IntegerField(verbose_name='Номер телефона')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Заявки'
        verbose_name_plural = 'Заявки'