from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(verbose_name='Название',max_length=100)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class Material(models.Model):
    title = models.CharField(verbose_name='Материал',max_length=30)
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Материалы'
        verbose_name_plural = 'Материалы'

class Product(models.Model):
    model = models.CharField(verbose_name='Модель',max_length=30)
    descriptoin = models.TextField(verbose_name='Описание',max_length=500)
    category = models.ManyToManyField(Category, verbose_name='Категория')
    material = models.ManyToManyField(Material, verbose_name='Материал', blank=True)
    resolution = models.CharField(verbose_name='Разрешение', max_length=20, blank=True)

    def __str__(self):
        return f'{self.model}'

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'

class PopularSolutions(models.Model):
    product = models.ManyToManyField(Product)