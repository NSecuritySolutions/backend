from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from product.models import ProductType


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Дата создания"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"), auto_now=True, blank=True, null=True
    )

    class Meta:
        abstract = True


class PriceList(BaseModel):
    file = models.FileField(_("Файл с прайс листом"), upload_to="media/price_list")

    class Meta:
        verbose_name = _("Прайс лист")
        verbose_name_plural = _("Прайс листы")

    def __str__(self):
        return f"{self.updated_at} - {self.file.name}"


class Calculator(BaseModel):
    """
    Модель калькулятора.

    Атрибуты:
        price_list (ForeignKey): Ссылка на прайс лист.
        is_active (bool): Флаг актуальности калькулятора.
    """

    active = models.BooleanField("Текущий калькулятор", default=False)
    price_list = models.ForeignKey(
        PriceList, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Калькулятор")
        verbose_name_plural = _("Калькуляторы")

    def __str__(self) -> str:
        return f"{self.pk}. Active" if self.active else f"{self.pk}"

    def clean(self) -> None:
        if self.active:
            prev_active_calc = Calculator.objects.filter(
                ~models.Q(pk=self.pk), active=True
            )
            if prev_active_calc:
                raise ValidationError(_("Только один калькулятор может быть активным."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class CalculatorBlock(BaseModel):
    """
    Модель блока калькулятора.

    Атрибуты:
        calculator (ForeignKey): Ссылка на калькулятор.
        position (int): Позиция блока в списке.
        title (str): Название блока.
        image (ImageField): Значок блока.
        main_product (ForeignKey): Главная категория товаров.
        formula (ForeignKey): Ссылка на формулу.
        quantity_selection (bool): Флаг выбора количества товара.
    """

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
    main_product = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        verbose_name=_("Категория главного товара"),
        help_text=_(
            "Если подходящего под условия товара не окажется, то значение всего блока будет 0."
        ),
        null=True,
        blank=True,
    )
    quantity_selection = models.BooleanField(
        verbose_name=_("Выбор кол-ва"),
        default=True,
        help_text=_(
            "Предоставить пользователю выбор кол-ва товара "
            "(иначе это будет выбор между 'да' и 'нет')"
        ),
    )

    class Meta:
        ordering = ("position",)
        verbose_name = _("Блок калькулятора")
        verbose_name_plural = _("Блоки калькулятора")

    def __str__(self) -> str:
        return f"{self.calculator}-{self.title}"


class Calculation(BaseModel):
    block = models.ForeignKey(
        CalculatorBlock, on_delete=models.CASCADE, related_name="calculations"
    )
    amount = models.TextField(
        _("Кол-во"),
        help_text=_(
            "Значение или формула для вычисления значения. Синтаксис math.js + функции:\n1. if(условие, значение при истино, значение при ложно)\n2. str_equals(строка, строка)"
        ),
    )
    product = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        verbose_name=_("Вид товара"),
        null=True,
    )
    filters = models.TextField(_("Фильтры для товара"), blank=True, null=True)

    class Meta:
        verbose_name = _("Вычисление")
        verbose_name_plural = _("Вычисления")

    def __str__(self) -> str:
        return f"{self.block}-{self.product}"


class BlockOption(PolymorphicModel, BaseModel):
    """
    Модель опции для блока калькулятора.

    Атрибуты:
        block (ForeignKey): Ссылка на блок калькулятора.
        position (int): Позиция опции в списке.
        title (str): Название опции.
        description (str): Описание опции.
        option_type (str): Тип опции (число, выбор, подтверждение, счетчик).
        choices (str): Варианты выбора для опции.
        depends_on (ForeignKey): Ссылка на опцию, от которой зависит текущая опция.
        depends_on_value (str): Значение, от которого зависит текущая опция.
    """

    class OptionTypes(models.TextChoices):
        NUMBER = ("number", _("Число"))
        RADIO = ("radio", _("Выбор"))
        CHECKBOX = ("checkbox", _("Подтверждение"))
        COUNTER = ("counter", _("Счетчик"))

    block = models.ForeignKey(
        CalculatorBlock, on_delete=models.CASCADE, related_name="options"
    )
    position = models.IntegerField(
        _("Позиция в списке"),
        validators=[MinValueValidator(1)],
    )
    title = models.CharField(_("Название"), max_length=40)
    description = models.CharField(_("Описание"))
    option_type = models.CharField(_("Тип опции"), choices=OptionTypes.choices)
    choices = models.CharField(
        _("Выбор"), blank=True, null=True, help_text=_("Перечислите варианты через ';'")
    )
    depends_on = models.ForeignKey(
        "BlockOption",
        on_delete=models.SET_NULL,
        verbose_name=_("Зависит от опции"),
        blank=True,
        null=True,
        related_name="dependent",
    )
    depends_on_value = models.CharField(
        _("Зависит от значения опции"), blank=True, null=True
    )
    variability_with_block_amount = models.BooleanField(
        _("Изменяется вместе с кол-вом в блоке)"),
        help_text=_("<strong>Только если опция числовая</strong>"),
        default=False,
    )
    initial_value = models.CharField(
        _("Начальное значение"),
        blank=True,
        null=True,
        help_text=_(
            "Если выбрана изменяемость, то это поле может быть только числом (по умолчанию равно 1). "
            "Иначе тут должно быть соответствующее типу опции значение "
            "(true, false - для подтверждения, один из вариантов - для выбора)"
        ),
    )

    class Meta:
        ordering = ("position",)
        verbose_name = _("Опция блока")
        verbose_name_plural = _("Опции блока")

    def __str__(self) -> str:
        return f"{self.block.calculator}-{self.block.title}. {self.title}"

    def clean(self) -> None:
        if self.depends_on is not None:
            if self.depends_on.pk == self.pk:
                raise ValidationError(
                    _("Нельзя сделать опцию зависимой от самой себя.")
                )
            if self.depends_on.block != self.block:
                raise ValidationError(
                    _("Опция, от которой зависим, должна быть из текущего блока.")
                )
        if self.variability_with_block_amount and self.option_type not in (
            "number",
            "counter",
        ):
            raise ValidationError(_("Опция должная быть числовой."))
        if self.initial_value:
            if (
                self.option_type in ("number", "counter")
                and not self.initial_value.isdigit()
            ):
                raise ValidationError(_("Начальное значение должно быть числом."))
            if self.option_type == "radio":
                is_ok = False
                for choice in self.choices.split(";"):
                    if choice.strip() == self.initial_value:
                        is_ok = True
                        break
                if not is_ok:
                    raise ValidationError(
                        _(
                            "Начальное значение должно соответствовать одному из вариантов."
                        )
                    )
            if self.option_type == "checkbox":
                if self.initial_value.lower() not in ("true", "false"):
                    raise ValidationError(
                        _("Начальное значение должно быть либо 'true', либо 'false'.")
                    )

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class ProductOption(BlockOption):
    """
    Модель опции товара для блока калькулятора.

    Атрибуты:
        block (ForeignKey): Ссылка на блок калькулятора.
        position (int): Позиция опции в списке.
        title (str): Название опции.
        description (str): Описание опции.
        option_type (str): Тип опции (число, выбор, подтверждение, счетчик).
        name (str): Имя поля модели.
        choices (str): Варианты выбора для опции.
        product (str): Название категории для фильтрации.
        filters (str): Фильтры для товара.
        depends_on (ForeignKey): Ссылка на опцию, от которой зависит текущая опция.
        depends_on_value (str): Значение, от которого зависит текущая опция.
        block_amount_undependent (bool): Флаг независимости кол-ва товара для опции от кол-ва в самом блоке.
        amount_depend (str): Название переменной в которой содержится кол-во для товара.
        variability_with_block_amount (bool): Флаг зависимости значения опции от кол-ва в самом блоке.
        initial_value (int): Начальное числовое значение.
    """

    name = models.CharField(
        _("Имя"),
        max_length=40,
        help_text=_(
            "Имя поля модели, или имя начинающееся на 'self' если тут происходит выбор "
            "кол-ва товара (поле будет называться <strong><данное имя>_&lt;id категории товара></strong>)"
        ),
    )
    product = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        verbose_name=_("Категория товара для фильтрации"),
        null=True,
        related_name="product_options",
    )
    filters = models.TextField(
        _("Фильтры для товара"),
        blank=True,
        null=True,
        help_text=_(
            "Фильтры перечисленые через запятую.\n"
            "Доступные операторы:\n"
            "1. Равенство: ==.\n"
            "2. Неравенство: !=.\n"
            "3. Больше: >.\n"
            "4. Меньше: <.\n"
            "5. Больше или равно: >=.\n"
            "6. Меньше или равно: <=.\n"
            "Пример: type == HD, price <= 1000"
        ),
    )
    block_amount_undependent = models.BooleanField(
        _("Кол-во товара не зависит от кол-ва в самом блоке"),
        default=False,
        help_text=_("Не будет учитываться если нет связи с категорией продукции"),
    )
    amount_depend = models.CharField(
        _("Кол-во товара зависит от переменной"),
        blank=True,
        null=True,
        help_text=_("Название переменной другой опции из этого блока"),
    )

    class Meta:
        verbose_name = "Опция с товаром"
        verbose_name_plural = "Опции с товарами"

    def clean(self) -> None:
        super().clean()
        if self.block_amount_undependent and self.amount_depend:
            option = BlockOption.objects.filter(
                block=self.block, name=self.amount_depend
            ).first()
            if option is None:
                raise ValidationError(
                    _("В блоке нет опции с данным именем переменной.")
                )
            if option.option_type not in ("number", "counter"):
                raise ValidationError(
                    _("Опция с данным именем переменной не является числовой опцией.")
                )
        if self.product is not None and not self.name.lower().startswith("self"):
            product_type = self.product
            found = False
            for property in product_type.properties.all():
                if self.name == property.field_name:
                    found = True
                    break
            if not found:
                raise ValidationError(
                    _("Такого поля у данного вида товара не существует")
                )
        if self.product and self.name.lower().startswith("self"):
            if self.pk:
                similar = ProductOption.objects.exclude(pk=self.pk).filter(
                    name__istartswith="self", product=self.product, block=self.block
                )
            else:
                similar = ProductOption.objects.filter(
                    name__istartswith="self", product=self.product, block=self.block
                )
            if len(similar) != 0:
                raise ValidationError(
                    _(
                        "Уже существует опция с выбором кол-ва для данной категории товара."
                    )
                )
            if self.option_type == "radio":
                choices = [part.strip() for part in self.choices.split(";")]
                for choice in choices:
                    if not choice.isdigit():
                        raise ValidationError(
                            _(
                                "При выборе кол-ва товара с возможностью выбора из предложенных "
                                "вариантов нельзя указвать нечисловые варианты."
                            )
                        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ValueOption(BlockOption):
    """
    Модель опции без товара для блока калькулятора.

    Атрибуты:
        block (ForeignKey): Ссылка на блок калькулятора.
        position (int): Позиция опции в списке.
        title (str): Название опции.
        description (str): Описание опции.
        option_type (str): Тип опции (число, выбор, подтверждение, счетчик).
        name (str): Имя переменной для формулы.
        choices (str): Варианты выбора для опции.
        depends_on (ForeignKey): Ссылка на опцию, от которой зависит текущая опция.
        depends_on_value (str): Значение, от которого зависит текущая опция.
        price (ForeignKey): Ссылка на цену.
        variability_with_block_amount (bool): Флаг зависимости значения опции от кол-ва в самом блоке.
        initial_value (int): Начальное числовое значение.
    """

    name = models.CharField(
        _("Имя"),
        max_length=40,
        help_text=_("Имя переменной для формул"),
    )
    # variability_with_block_amount = models.BooleanField(
    #     _("Изменяется вместе с кол-вом в блоке"),
    #     default=False,
    # )
    # initial_value = models.IntegerField(
    #     _("Начальное числовое значение"),
    #     blank=True,
    #     null=True,
    #     help_text=_(
    #         "Можно оставить пустым для 1 (при условии, что выбрана изменяемость)"
    #     ),
    # )

    class Meta:
        verbose_name = "Опция со значением"
        verbose_name_plural = "Опции со значениями"

    # def clean(self) -> None:
    #     super().clean()
    #     if self.variability_with_block_amount and self.option_type not in (
    #         "counter",
    #         "number",
    #     ):
    #         raise ValidationError(
    #             _("Изменяемость работает только с числовыми опциями.")
    #         )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
