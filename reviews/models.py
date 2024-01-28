from django.db import models

# Create your models here.
class Reviews(models.Model):
    name = models.CharField(verbose_name='Отзыв', max_length=20)