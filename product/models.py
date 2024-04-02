from django.db import models
from django.utils import timezone
tz = timezone.get_default_timezone()


# Create your models here.

#ответы и вопросы

class Category(models.Model):
    title = models.CharField(verbose_name='Категория', max_length=20)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class Manufacturer(models.Model):
    title = models.CharField(verbose_name='Производитель', max_length=20)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Производителя'
        verbose_name_plural = 'Производители'

class Product(models.Model):
    FORM_FACTOR_CHOICES = (
        ('Domed', 'Купольная'),
        ('Cylindrical', 'Цилиндрическая'),
    )

    ACCOMMODATION_CHOICES = (
        ('Street', 'Уличное'),
        ('Internal', 'Внутренняя'),
    )

    MICROPHONE_CHOICES = (
        ('No', 'Нет'),
        ('Microphone', 'Микрофон'),
        ('Microphone_speaker', 'Микрофон/Динамик')
    )

    article = models.CharField(verbose_name='Артикул',max_length=50)
    model = models.CharField(verbose_name='Модель',max_length=300)
    image = models.ImageField(verbose_name="Изображение", upload_to="media/camera")
    description = models.CharField(verbose_name='Описание',max_length=200)
    form_factor = models.CharField(verbose_name='Форм Фактор', max_length=20, choices=FORM_FACTOR_CHOICES)
    manufacturer = models.ManyToManyField(Manufacturer,verbose_name='Производитель')
    accommodation = models.CharField(verbose_name='Размещение',max_length=30, choices=ACCOMMODATION_CHOICES)
    resolution = models.CharField(verbose_name='Разрешение',max_length=30)
    dark = models.CharField(verbose_name='Съемка в темноте',max_length=30)
    temperature = models.CharField(verbose_name='Температура',max_length=30)
    nutrition = models.CharField(verbose_name='Питание',max_length=30)
    microphone = models.CharField(verbose_name='Микрофон',max_length=30, choices=MICROPHONE_CHOICES)
    micro_sd = models.CharField(verbose_name='MicroSD',max_length=30)
    viewing_angle = models.CharField(verbose_name='Угол Обзора',max_length=30)
    focus = models.CharField(verbose_name='Фокус',max_length=30)
    category = models.ManyToManyField(Category,verbose_name='Категория')
    price = models.IntegerField(verbose_name="Цена", default=0)


    def __str__(self):
        return f'{self.model}'

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'

class ReadySolutions(models.Model):
    title = models.CharField(verbose_name='Предложение', max_length=100)
    product = models.ManyToManyField(Product, verbose_name='Продукт')
    description = models.TextField(verbose_name ="Полное описание", max_length=300)
    short_description = models.CharField(verbose_name='Краткое описание', max_length=50)
    price = models.IntegerField(verbose_name='Итог', null= True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Готовые решение'
        verbose_name_plural = 'Готовые решение'


class OurService(models.Model):
    image = models.ImageField(verbose_name='Фотография',upload_to='media/service')
    description = models.TextField(verbose_name='Описание',max_length=500)

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'Наши услуги'
        verbose_name_plural = 'Наши услуги'

class Image_Works(models.Model):
    image = models.ImageField(verbose_name="Фотографии",upload_to='media/our_works')

    def __str__(self):
        return f'Image {self.image}'
    
    class Meta:
        verbose_name = 'Фотографии'
        verbose_name_plural = 'Фотографии'

class OurWorks(models.Model):
    image = models.ManyToManyField(Image_Works, verbose_name='Фотография')
    description = models.TextField(verbose_name='Описание',max_length=500)
    product = models.TextField(verbose_name='Продукт',max_length=500)
    price = models.IntegerField(verbose_name="Цена", primary_key=True)
    date_works = models.DateTimeField(verbose_name="Дата начало проекта")
    date_finish = models.DateTimeField(verbose_name="Дата окончание проекта")
    add_date = models.DateTimeField(verbose_name='Дата добавление на сайт')

    def date_two(self):
        return self.date_works.strftime('%d.%m.%Y')
    
    def date_three(self):
        return self.date_finish.strftime('%d.%m.%Y')
    
    def date_one(self):
        return self.add_date.strftime('%d.%m.%Y')
    
    def __str__(self):
        return f'{self.descriptoin}'

    class Meta:
        verbose_name = 'Примеры работ'
        verbose_name_plural = 'Примеры работ'



