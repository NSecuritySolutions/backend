from django.db import models

# Create your models here.


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="ФИО", max_length=20)
    description = models.TextField(
        verbose_name="Комментарий", max_length=500, null=True, blank=True
    )
    email = models.EmailField(verbose_name="Почта", blank=True)
    number = models.IntegerField(verbose_name="Номер телефона")
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Заявки"
        verbose_name_plural = "Заявки"
