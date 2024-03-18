from django.db import models


# Create your models here.


class Camera(models.Model):
    TIME_CHOICES =(
        ('7', '7'),
        ('14', '14'),
        ('30', '30')
    )

    TYPE_SYSTEM_CHOICES = (
        ('AHD', 'AHD'),
        ('IP', 'IP')
    )

    QUALITY_CHOICES = (
        ('HD', 'HD'),
        ('FullHD', 'FullHD'),
        ('2K-4K', '2K-4K')
    )
    id = models.AutoField(primary_key=True)


    time = models.CharField(verbose_name='Время хранение видео',max_length=5, choices=TIME_CHOICES)
    system_type = models.CharField(verbose_name='Тип системы',max_length=4, choices=TYPE_SYSTEM_CHOICES)
    quality = models.CharField(verbose_name='Качество изображения',max_length=6, choices=QUALITY_CHOICES)
    external = models.IntegerField(verbose_name='Внешние',default=0)
    domestic = models.IntegerField(verbose_name='Внутренние',default=0)
    total_price = models.IntegerField(verbose_name='Итог', null= True, blank=True)

    def __str__(self):
        return f'Конфигурация {self.id}'

    class Meta:
        verbose_name = 'Конфигурации камер'
        verbose_name_plural = 'Конфигурации камер'



class CameraPrice(models.Model):
    seven = models.IntegerField(verbose_name='Внешние')
    fourteen = models.IntegerField()
    thirty = models.IntegerField()

    ahd = models.IntegerField()
    ip = models.IntegerField()

    hd = models.IntegerField()
    fullhd = models.IntegerField()
    two_k = models.IntegerField()

    external = models.IntegerField(verbose_name='Внешние',default=0)
    domestic = models.IntegerField(verbose_name='Внутренние',default=0)

    def __str__(self):
        return f'Цены на камеры'

    class Meta:
        verbose_name = 'Цены на камеры'
        verbose_name_plural = 'Цены на камеры'
