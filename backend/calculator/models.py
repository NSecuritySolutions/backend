from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from calculator.validators import validate_latin_underscore


class PriceList(models.Model):
    """Модель прайс листа."""

    date = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Прайс лист")
        verbose_name_plural = _("Прайс листы")

    def __str__(self):
        return f"{self.pk}. Created at {self.date}"


class Price(models.Model):
    """Модель цены."""

    price_list = models.ForeignKey(
        PriceList, on_delete=models.SET_NULL, null=True, related_name="prices"
    )
    name = models.CharField("Название услуги/товара")
    variable_name = models.CharField(
        _("Переменная"),
        max_length=200,
        help_text=_(
            "Имя переменной в калькуляторе (латинские символы, цифры и нижнее подчеркивание)"
        ),
        blank=True,
        null=True,
        validators=[validate_latin_underscore],
    )
    price = models.IntegerField(_("Цена"), validators=[MinValueValidator(0)])
    is_show = models.BooleanField(
        _("Показывать клиенту"), help_text=_("Отображать ли эту цену в прайс листе")
    )


class Formula(models.Model):
    """Модель формулы для калькулятора."""

    expression = models.TextField(
        _("Формула"),
        help_text=_(
            "Синтаксис math.js + функции:\n1. if(условие, значение при истино, значение при ложно)\n2. str_equals(строка, строка)"
        ),
    )

    class Meta:
        verbose_name = _("Формула")
        verbose_name_plural = _("Формулы")

    def __str__(self) -> str:
        return self.expression


class Calculator(models.Model):
    """Модель калькулятора."""

    price_list = models.ForeignKey(
        PriceList, on_delete=models.SET_NULL, blank=True, null=True
    )
    is_active = models.BooleanField("Текущий калькулятор", default=False)

    class Meta:
        verbose_name = _("Калькулятор")
        verbose_name_plural = _("Калькуляторы")

    def __str__(self) -> str:
        return f"{self.pk}. Active" if self.is_active else f"{self.pk}"

    def clean(self) -> None:
        if self.is_active:
            prev_active_calc = Calculator.objects.filter(
                ~models.Q(pk=self.pk), is_active=True
            )
            if prev_active_calc:
                raise ValidationError(_("Только один калькулятор может быть активным."))


class CalculatorBlock(models.Model):
    """Модель блока калькулятора."""

    calculator = models.ForeignKey(
        Calculator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="blocks",
    )
    position = models.IntegerField(
        _("Позиция в списке"), validators=[MinValueValidator(1)]
    )
    title = models.CharField(_("Название"), max_length=40)
    image = models.ImageField(
        _("Значок"), upload_to="media/calculator", blank=True, null=True, default=None
    )
    formula = models.ForeignKey(
        Formula, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity_selection = models.BooleanField(
        verbose_name=_("Выбор кол-ва"),
        default=True,
        help_text=_(
            "Предоставить пользователю выбор кол-ва товара (иначе это будет выбор между 'да' и 'нет')"
        ),
    )

    class Meta:
        ordering = ("position",)
        verbose_name = _("Блок калькулятора")
        verbose_name_plural = _("Блоки калькулятора")

    def __str__(self) -> str:
        return f"{self.calculator}-{self.title}"

    def clean(self) -> None:
        count = CalculatorBlock.objects.filter(calculator=self.calculator).count()
        if self.pk is None:
            count += 1
        if self.position > count:
            raise ValidationError(
                _("Позиция не должна превышать кол-во блоков у калькулятора.")
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class BlockOption(models.Model):
    """Модель опции для блока калькулятора."""

    class OptionTypes(models.TextChoices):
        NUMBER = ("number", _("Число"))
        RADIO = ("radio", _("Выбор"))
        CHECKBOX = ("checkbox", _("Подтверждение"))
        COUNTER = ("counter", _("Счетчик"))

    block = models.ForeignKey(
        CalculatorBlock, on_delete=models.CASCADE, related_name="options"
    )
    position = models.IntegerField(
        _("Позиция в списке"), validators=[MinValueValidator(1)]
    )
    title = models.CharField(_("Название"), max_length=40)
    description = models.CharField(_("Описание"))
    option_type = models.CharField(_("Тип опции"), choices=OptionTypes.choices)
    name = models.CharField(
        _("Имя"),
        max_length=40,
        help_text=_("Имя переменной для формулы или имя поля модели"),
    )
    choices = models.CharField(
        _("Выбор"), blank=True, null=True, help_text=_("Перечислите варианты через ';'")
    )
    product = models.CharField(
        _("Продукт для фильтрации"),
        blank=True,
        null=True,
        help_text=_("Название категории"),
    )
    filters = models.TextField(
        _("Фильтры для товара"),
        blank=True,
        null=True,
        help_text=_(
            "Фильтры перечисленые через запятую.\nДоступные операторы:\n1. Равенство: ==.\n2. Неравенство: !=.\n3. Больше: >.\n4. Меньше: <.\n5. Больше или равно: >=.\n6. Меньше или равно: <=.\nПример: type == HD, price <= 1000"
        ),
    )

    class Meta:
        ordering = ("position",)
        verbose_name = _("Опция для блока")
        verbose_name_plural = _("Опции блока")

    def __str__(self) -> str:
        return f"{self.block.calculator}-{self.block.title}. {self.title}"

    def clean(self) -> None:
        count = BlockOption.objects.filter(block=self.block).count()
        if self.pk is None:
            count += 1
        if self.position > count:
            raise ValidationError(
                _("Позиция не должна превышать кол-во опций у блока.")
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
