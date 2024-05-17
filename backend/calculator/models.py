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

    def __str__(self):
        return f"{self.pk}. Active: {self.is_current}"


class Formula(models.Model):
    """Модель формулы для калькулятора."""
    expression = models.CharField(_("Формула"))

    class Meta:
        verbose_name = _("Формула")
        verbose_name_plural = _("Формулы")

    def __str__(self) -> str:
        return self.expression


class Calculator(models.Model):
    """Модель калькулятора."""
    price_list = models.ForeignKey(PriceList, on_delete=models.SET_NULL, blank=True, null=True)
    formula = models.ForeignKey(Formula, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _("Калькулятор")
        verbose_name_plural = _("Калькуляторы")

    def __str__(self) -> str:
        return f"{self.pk}"


class CalculatorBlock(models.Model):
    """Модель блока калькулятора."""
    calculator = models.ForeignKey(Calculator, on_delete=models.SET_NULL, blank=True, null=True, related_name='blocks')
    title = models.CharField(_('Название'), max_length=40)
    image = models.ImageField(_('Значок'), upload_to='media/calculator', blank=True, null=True, default=None)

    class Meta:
        verbose_name = _("Блок калькулятора")
        verbose_name_plural = _("Блоки калькулятора")

    def __str__(self) -> str:
        return f"{self.calculator}-{self.title}"


class BlockOption(models.Model):
    """Модель опции для блока калькулятора."""
    class OptionTypes(models.TextChoices):
        NUMBER = ('number', _('Число'))
        RADIO = ('radio', _('Выбор'))
        CHECKBOX = ('checkbox', _('Подтверждение'))

    block = models.ForeignKey(CalculatorBlock, on_delete=models.CASCADE, related_name='options')
    title = models.CharField(_('Название'), max_length=40)
    description = models.CharField(_('Описание'))
    option_type = models.CharField(_('Тип опции'), choices=OptionTypes.choices)
    name = models.CharField(_('Имя'), max_length=40, help_text=_('Имя переменной для формулы'))
    choices = models.CharField(_('Выбор'), blank=True, null=True, help_text=_("Перечислите варианты через ';'"))

    class Meta:
        verbose_name = _("Опция для блока")
        verbose_name_plural = _("Опции блока")

    def __str__(self) -> str:
        return f"{self.block.calculator}-{self.block.title}. {self.title}"
