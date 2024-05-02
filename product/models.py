from django.db import models
from django.utils import timezone
tz = timezone.get_default_timezone()


# Create your models here.

class Questions(models.Model):
    CATEGORY_CHOICES = (
        ('Общие Вопросы','Общие Вопросы'),
        ('Вопросы по видеонаблюдению', 'Вопросы по видеонаблюдению'),
        ('Вопросы по домофонии', 'Вопросы по домофонии'),
        ('Вопросы по биометрии и системам контроля учёта доступа','Вопросы по биометрии и системам контроля учёта доступа'),
        ('Вопросы по шлагбаумам и турникетам (в СКУД)','Вопросы по шлагбаумам и турникетам (в СКУД)'),
        ('Вопросы по охранно-пожарной сигнализации','Вопросы по охранно-пожарной сигнализации')
        )
    questions = models.CharField(verbose_name='Вопрос', max_length=200)
    answer = models.TextField(verbose_name='Ответ', max_length=500)
    category = models.CharField(verbose_name='Категории',choices=CATEGORY_CHOICES) 

    class Meta:
        verbose_name = 'Вопрос/Ответ'
        verbose_name_plural = 'Вопрос/Ответ'

    
    def __str__(self):
        return f'{self.questions}'


class Category(models.Model):
    title = models.CharField(verbose_name='Категория', max_length=50)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class Manufacturer(models.Model):
    title = models.CharField(verbose_name='Производитель', max_length=50)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Производителя'
        verbose_name_plural = 'Производители'

class Product(models.Model):
    article = models.CharField(verbose_name='Артикул',max_length=100)
    model = models.CharField(verbose_name='Модель',max_length=300)
    image = models.ImageField(verbose_name="Изображение", upload_to="media/camera")
    type = models.CharField(verbose_name='Тип', max_length=20)
    description = models.CharField(verbose_name='Описание',max_length=5000)
    form_factor = models.CharField(verbose_name='Форм Фактор', max_length=20)
    manufacturer = models.ManyToManyField(Manufacturer,verbose_name='Производитель')
    accommodation = models.CharField(verbose_name='Размещение',max_length=30)
    resolution = models.CharField(verbose_name='Разрешение',max_length=30)
    dark = models.CharField(verbose_name='Съемка в темноте',max_length=30)
    temperature = models.CharField(verbose_name='Температура',max_length=30)
    nutrition = models.CharField(verbose_name='Питание',max_length=30)
    microphone = models.CharField(verbose_name='Микрофон',max_length=30)
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


class Register(models.Model):
    article = models.CharField(verbose_name='Артикул',max_length=100)
    model = models.CharField(verbose_name='Модель',max_length=300)
    image = models.ImageField(verbose_name="Изображение", upload_to="media/register")
    description = models.CharField(verbose_name='Описание',max_length=5000)
    manufacturer = models.ManyToManyField(Manufacturer,verbose_name='Производитель')
    max_resolution = models.CharField(verbose_name='Максимально разрешение',max_length=50)
    quantity_сam = models.IntegerField(verbose_name='Количество камер')
    quantity_hdd = models.IntegerField(verbose_name='Количество hhd')
    max_quantity_hdd = models.IntegerField(verbose_name='Макс объем HDD Тб')
    nutrition = models.CharField(verbose_name='Питание',max_length=50)
    price = models.IntegerField(verbose_name="Цена", default=0)

    def __str__(self):
        return f'{self.model}'
    
    class Meta:
        verbose_name = 'Регистраторы'
        verbose_name_plural = 'Регистраторы'


class HDD(models.Model):
    model = models.CharField(verbose_name='Модель',max_length=300)
    description = models.CharField(verbose_name='Описание',max_length=200)
    manufacturer = models.ManyToManyField(Manufacturer,verbose_name='Производитель')
    price = models.IntegerField(verbose_name="Цена", default=0)

    def __str__(self):
        return f'{self.model}'
    
    class Meta:
        verbose_name = 'HDD'
        verbose_name_plural = 'HDD'


class ReadySolutions(models.Model):
    image = models.ImageField(verbose_name='Фотография', upload_to='media/ready')
    title = models.CharField(verbose_name='Предложение', max_length=300)
    description = models.TextField(verbose_name ="Описание", max_length=5000)
    short_description = models.CharField(verbose_name='Краткое описание', max_length=200)
    price = models.IntegerField(verbose_name='Цена', null= True, blank=True)
    category = models.ManyToManyField(Category,verbose_name='Категории')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Готовые решение'
        verbose_name_plural = 'Готовые решение'


class OurService(models.Model):
    image = models.ImageField(verbose_name='Фотография',upload_to='media/service')
    title = models.CharField(verbose_name='название', max_length=400)
    description = models.TextField(verbose_name='Описание',max_length=5000)

    def __str__(self):
        return f'{self.title}'

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
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='Предложение', max_length=300)
    main_image = models.ImageField(verbose_name='Фотография', upload_to='media/ourworks')
    image = models.ManyToManyField(Image_Works, verbose_name='Фотографии')
    product = models.TextField(verbose_name='Используемое оборудование',max_length=5000)
    description = models.TextField(verbose_name='Описание',max_length=5000)
    add_date = models.DateTimeField(verbose_name='Дата добавление на сайт')
    deadline = models.IntegerField(verbose_name='Сроки')
    budget = models.IntegerField(verbose_name='Бюджет')
    equipped = models.IntegerField(verbose_name='Оборудовано')


    
    def date(self):
        return self.add_date.strftime('%d.%m.%Y')
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Примеры работ'
        verbose_name_plural = 'Примеры работ'



