from django.db import models


# Create your models here.


class Camera(models.Model):
    TIME_CHOICES =(
        ('one', '7'),
        ('two', '14'),
        ('three', '30')
    )


    time = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
