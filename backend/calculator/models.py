from django.db import models
from django.utils.translation import gettext_lazy as _


class PriceList(models.Model):
    """Модель прайс листа."""

    # Cameras

    # Inner camera prices
    setup_inner_camera_easy = models.IntegerField(_("Простая установка внутренней камеры"))
    setup_inner_camera = models.IntegerField(_("Установка внутренней камеры"))
    setup_inner_camera_hard = models.IntegerField(_("Сложная установка внутренней камеры"))
    cabel_price_for_inner_cameras_per_meter = models.IntegerField(_("Цена за 1 метра кабеля для внутренних камер"))

    # Outer camera prices
    setup_outer_camera_easy = models.IntegerField(_("Простая установка внешней камеры"))
    setup_outer_camera = models.IntegerField(_("Установка внешней камеры"))
    setup_outer_camera_hard = models.IntegerField(_("Сложная установка внешней камеры"))
    cabel_price_for_outer_cameras_per_meter = models.IntegerField(_("Цена за 1 метра кабеля для внешних камер"))

    # Additional setup for cameras
    setup_ahd_registery = models.IntegerField(_("Установка регистратора AHD системы"))
    setup_ip_registery = models.IntegerField(_("Установка регистратора IP системы"))
    price_multiplier_for_registery_setup = models.IntegerField(_("Множитель цены установки регистратора если больше 16 камер"))
    registery_4 = models.IntegerField(_("Цена регистратора при 4 и меньше камерах"))
    registery_8 = models.IntegerField(_("Цена регистратора при 4 и меньше камерах"))
    registery_16 = models.IntegerField(_("Цена регистратора при 4 и меньше камерах"))
    registery_20 = models.IntegerField(_("Цена регистратора при 4 и меньше камерах"))
    registery_24 = models.IntegerField(_("Цена регистратора при 4 и меньше камерах"))
    registery_32 = models.IntegerField(_("Цена регистратора при 4 и меньше камерах"))
    power_unit = models.IntegerField(_("Цена блока питания с работой (цена увеличивается каждые 5 камер)"))

    is_current = models.BooleanField(_("Актуальный прайс лист"), default=False)

    class Meta:
        verbose_name = _("Прайс лист")
        verbose_name_plural = _("Прайс листы")
