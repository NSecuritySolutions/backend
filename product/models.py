from django.db import models
from django.utils import timezone
tz = timezone.get_default_timezone()

import datetime


# Create your models here.

class Product(models.Model):
    model = models.CharField(verbose_name='Модель',max_length=30)
    image = models.ImageField(verbose_name="Изображение", upload_to="media/camera")
    descriptoin = models.TextField(verbose_name='Описание',max_length=500)
    manufacturer = models.CharField(verbose_name='Производитель', max_length=30)
    accommodation = models.CharField(verbose_name='Размещение',max_length=30)
    resolution = models.CharField(verbose_name='Разрешение',max_length=30)
    dark = models.CharField(verbose_name='Съемка в темноте',max_length=30)
    temperature = models.CharField(verbose_name='Температура',max_length=30)
    nutrition = models.CharField(verbose_name='Питание',max_length=30)
    microphone = models.CharField(verbose_name='Микрофон',max_length=30)
    micro_sd = models.CharField(verbose_name='MicroSD',max_length=30)
    viewing_angle = models.CharField(verbose_name='Угол Обзора',max_length=30)
    focus = models.CharField(verbose_name='Фокус',max_length=30)
    category = models.CharField(verbose_name='Категория',max_length=30)
    price = models.IntegerField(verbose_name="Цена", primary_key=True)


    def __str__(self):
        return f'{self.model}'

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'

class PopularSolutions(models.Model):
    name = models.CharField(verbose_name='Предложение', max_length=100)
    product = models.ManyToManyField(Product, verbose_name='Популярный продукт')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Готовые решение'
        verbose_name_plural = 'Готовые решение'



class OurService(models.Model):
    image = models.ImageField(verbose_name='Фотография',upload_to='media/service')
    descriptoin = models.TextField(verbose_name='Описание',max_length=500)

    def __str__(self):
        return f'{self.descriptoin}'

    class Meta:
        verbose_name = 'Наши услуги'
        verbose_name_plural = 'Наши услуги'

class Image_Works(models.Model):
    image = models.ImageField(verbose_name="Фотографии",upload_to='media/our_works')

    def __str__(self):
        return f'Image {self.id}'

class OurWorks(models.Model):
    image = models.ManyToManyField(Image_Works, verbose_name='Фотография')
    descriptoin = models.TextField(verbose_name='Описание',max_length=500)
    price = models.IntegerField(verbose_name="Цена", primary_key=True)
    date_works = models.DateTimeField(verbose_name="Дата выполнение проекта")
    add_date = models.DateTimeField(verbose_name='Дата добавление на сайт')

    def date_two(self):
        return self.date_works.strftime('%d.%m.%Y')
    
    def date_one(self):
        return self.add_date.strftime('%d.%m.%Y')
    
    def __str__(self):
        return f'{self.descriptoin}'

    class Meta:
        verbose_name = 'Примеры работ'
        verbose_name_plural = 'Примеры работ'



