from django.db import models


class PriceList(models.Model):
    """Модель прайс листа."""
    setup_inner_camera_easy = models.IntegerField("Простая установка внутренней камеры")
    setup_inner_camera = models.IntegerField("Установка внутренней камеры")
    setup_inner_camera_hard = models.IntegerField("Сложная установка внутренней камеры")
    cabel_price_for_inner_cameras_per_meter = models.IntegerField("Цена за 1 метра кабеля для внутренних камер")
    setup_outer_camera_easy = models.IntegerField("Простая установка внешней камеры")
    setup_outer_camera = models.IntegerField("Установка внешней камеры")
    setup_outer_camera_hard = models.IntegerField("Сложная установка внешней камеры")
    cabel_price_for_outer_cameras_per_meter = models.IntegerField("Цена за 1 метра кабеля для внешних камер")
    setup_ahd_registery = models.IntegerField("Установка регистратора AHD системы")
    setup_ip_registery = models.IntegerField("Установка регистратора IP системы")
    price_multiplier_for_registery_setup = models.IntegerField("Множитель цены установки регистратора если больше 16 камер")
    registery_4 = models.IntegerField("Цена регистратора при 4 и меньше камерах")
    registery_8 = models.IntegerField("Цена регистратора при 4 и меньше камерах")
    registery_16 = models.IntegerField("Цена регистратора при 4 и меньше камерах")
    registery_20 = models.IntegerField("Цена регистратора при 4 и меньше камерах")
    registery_24 = models.IntegerField("Цена регистратора при 4 и меньше камерах")
    registery_32 = models.IntegerField("Цена регистратора при 4 и меньше камерах")
    power_unit = models.IntegerField("Цена блока питания с работой (цена увеличивается каждые 5 камер)")

    class Meta:
        verbose_name = "Прайс лист"


class Camera(models.Model):
    TIME_CHOICES = (("7", "7"), ("14", "14"), ("30", "30"))

    TYPE_SYSTEM_CHOICES = (("AHD", "AHD"), ("IP", "IP"))

    QUALITY_CHOICES = (("HD", "HD"), ("FullHD", "FullHD"), ("2K-4K", "2K-4K"))
    id = models.AutoField(primary_key=True)

    time = models.CharField(
        verbose_name="Время хранение видео", max_length=5, choices=TIME_CHOICES
    )
    system_type = models.CharField(
        verbose_name="Тип системы", max_length=4, choices=TYPE_SYSTEM_CHOICES
    )
    quality = models.CharField(
        verbose_name="Качество изображения", max_length=6, choices=QUALITY_CHOICES
    )
    external = models.IntegerField(verbose_name="Внешние", default=0)
    domestic = models.IntegerField(verbose_name="Внутренние", default=0)
    total_price = models.IntegerField(verbose_name="Итог", null=True, blank=True)

    def __str__(self):
        return f"Конфигурация {self.id}"

    class Meta:
        verbose_name = "Конфигурации камер"
        verbose_name_plural = "Конфигурации камер"


class CameraPrice(models.Model):
    seven = models.IntegerField(verbose_name="Внешние")
    fourteen = models.IntegerField()
    thirty = models.IntegerField()

    ahd = models.IntegerField()
    ip = models.IntegerField()

    hd = models.IntegerField()
    fullhd = models.IntegerField()
    two_k = models.IntegerField()

    external = models.IntegerField(verbose_name="Внешние", default=0)
    domestic = models.IntegerField(verbose_name="Внутренние", default=0)

    def __str__(self):
        return f"Цены на камеры"

    class Meta:
        verbose_name = "Цены на камеры"
        verbose_name_plural = "Цены на камеры"
