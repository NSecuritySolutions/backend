from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from calculator.validators import validate_latin_underscore
from product.models import Product, ProductCategory


class PriceList(models.Model):
    """
    Модель прайс листа.

    Атрибуты:
        date (DateTimeField): Дата создания прайс листа.
    """

    date = models.DateTimeField(_("Дата последнего обновления"), auto_now_add=True)

    class Meta:
        verbose_name = _("Прайс лист")
        verbose_name_plural = _("Прайс листы")

    def __str__(self):
        return f"{self.pk}. Updated at {self.date}"


class PriceListCategory(models.Model):
    """
    Модель катогрии для прайс листа.

    Атрибуты:
                name (str): Название категории.
        price_list (ForeignKey): Ссыслка на прайс лист.
    """

    name = models.CharField(_("Название"), max_length=100)
    price_list = models.ForeignKey(
        PriceList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="categories",
    )

    class Meta:
        verbose_name = _("Категория прайс листа")
        verbose_name_plural = _("Категории прайс листов")

    def __str__(self) -> str:
        return self.name


class Price(models.Model):
    """
    Модель цены.

    Атрибуты:
        price_list_category (ForeignKey): Ссылка на категорию прайс листа.
        name (str): Название услуги/товара.
        variable_name (str): Имя переменной в калькуляторе.
        price (int): Цена услуги/товара.
        is_show (bool): Флаг отображения цены клиенту.
    """

    price_list_category = models.ForeignKey(
        PriceListCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="prices",
        blank=True,
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
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Связать с ценой товара"),
        related_name="prices_in_price_lists",
    )
    is_show = models.BooleanField(
        _("Показывать клиенту"), help_text=_("Отображать ли эту цену в прайс листе")
    )

    class Meta:
        verbose_name = _("Цена")
        verbose_name_plural = "Цены"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if self.product:
            self.price = self.product.price
        return super().save(*args, **kwargs)


class Formula(models.Model):
    """
    Модель формулы для калькулятора.

    Атрибуты:
        name (str): Название формулы.
        expression (str): Формула в синтаксисе math.js с дополнительными функциями.
    """

    name = models.CharField(_("Название"), max_length=100)
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
        return self.name


class Calculator(models.Model):
    """
    Модель калькулятора.

    Атрибуты:
        price_list (ForeignKey): Ссылка на прайс лист.
        is_active (bool): Флаг актуальности калькулятора.
    """

    price_list = models.ForeignKey(
        PriceList, on_delete=models.SET_NULL, blank=True, null=True
    )
    active = models.BooleanField("Текущий калькулятор", default=False)

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


class CalculatorBlock(models.Model):
    """
    Модель блока калькулятора.

    Атрибуты:
        calculator (ForeignKey): Ссылка на калькулятор.
        position (int): Позиция блока в списке.
        title (str): Название блока.
        image (ImageField): Значок блока.
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
    formula = models.ForeignKey(
        Formula, on_delete=models.SET_NULL, blank=True, null=True
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


# TODO нужно ли???
# def clean(self) -> None:
#     count = CalculatorBlock.objects.filter(calculator=self.calculator).count()
#     if self.pk is None:
#         count += 1
#     if self.position > count:
#         raise ValidationError(
#             _("Позиция не должна превышать кол-во блоков у калькулятора.")
#         )

# def save(self, *args, **kwargs):
#     self.clean()
#     super().save(*args, **kwargs)


class BlockOption(models.Model):
    """
    Модель опции для блока калькулятора.

    Атрибуты:
        block (ForeignKey): Ссылка на блок калькулятора.
        position (int): Позиция опции в списке.
        title (str): Название опции.
        description (str): Описание опции.
        option_type (str): Тип опции (число, выбор, подтверждение, счетчик).
        name (str): Имя переменной для формулы или имя поля модели.
        choices (str): Варианты выбора для опции.
        product (str): Название категории для фильтрации.
        filters (str): Фильтры для товара.
        depends_on (ForeignKey): Ссылка на опцию, от которой зависит текущая опция.
        depends_on_value (str): Значение, от которого зависит текущая опция.
        price (ForeignKey): Ссылка на цену.
        block_amount_undependent (bool): Флаг независимости кол-ва товара для опции от кол-ва в самом блоке.
        amount_depend (str): Название переменной в которой содержится кол-во для товара.
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
    name = models.CharField(
        _("Имя"),
        max_length=40,
        help_text=_("Имя переменной для формулы или имя поля модели"),
    )
    choices = models.CharField(
        _("Выбор"), blank=True, null=True, help_text=_("Перечислите варианты через ';'")
    )
    product = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        verbose_name=_("Категория продукта для фильтрации"),
        blank=True,
        null=True,
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
    depends_on = models.ForeignKey(
        "BlockOption",
        on_delete=models.SET_NULL,
        verbose_name=_("Зависит от опции"),
        blank=True,
        null=True,
        related_name="dependent",
    )
    depends_on_value = models.CharField(_("Зависит от значения опции"), blank=True)
    price = models.ForeignKey(
        Price,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Связать с ценой из прайс листа"),
    )
    block_amount_undependent = models.BooleanField(
        _("Не зависит от кол-ва в самом блоке"), default=False
    )
    amount_depend = models.CharField(
        _("Зависит от переменной"),
        blank=True,
        null=True,
        help_text=_("Название переменной другой опции из этого блока"),
    )

    class Meta:
        ordering = ("position",)
        verbose_name = _("Опция для блока")
        verbose_name_plural = _("Опции блока")

    def __str__(self) -> str:
        return f"{self.block.calculator}-{self.block.title}. {self.title}"

    def clean(self) -> None:
        # TODO нужно ли???
        # count = BlockOption.objects.filter(block=self.block).count()
        # if self.pk is None:
        #     count += 1
        # if self.position > count:
        #     raise ValidationError(
        #         _("Позиция не должна превышать кол-во опций у блока.")
        #     )
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
                    _("Опция с данным именем переменной не содержит число.")
                )
        if self.price and self.product:
            raise ValidationError(
                _(
                    "Нельзя связать с категорией товара и ценой из прайс листа одновременно."
                )
            )
        if self.depends_on is not None:
            if self.depends_on.pk == self.pk:
                raise ValidationError(
                    _("Нельзя сделать опцию зависимой от самой себя.")
                )
            if self.depends_on.block != self.block:
                raise ValidationError(
                    _("Опция, от которой зависим, должна быть из текущего блока.")
                )
        if self.product is not None:
            products = Product.objects.filter(
                category__title=self.product
            ).get_real_instances()
            found = False
            for product in products:
                if self.name in map(
                    lambda x: x.attname, product._meta._get_fields(reverse=False)
                ):
                    found = True
                    break
            if not found:
                raise ValidationError(
                    _("Такого поля у данной категории моделей не существует")
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
