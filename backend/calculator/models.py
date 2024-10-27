from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from calculator.validators import validate_latin_underscore
from product.models import Product


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
    """
    Модель прайс листа.

    Атрибуты:
        created_at (DateTimeField): Дата создания прайс листа.
        updated_at (DateTimeField): Дата последнего изменения.
    """

    created_at = models.DateTimeField(
        _("Дата создания"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"), auto_now=True, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Прайс лист")
        verbose_name_plural = _("Прайс листы")

    def __str__(self):
        return f"{self.pk}. Updated at {self.updated_at}"


class PriceListCategory(BaseModel):
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


class Price(BaseModel):
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


class Formula(BaseModel):
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


class Calculator(BaseModel):
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


class CalculatorBlock(BaseModel):
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
    depends_on_value = models.CharField(_("Зависит от значения опции"), blank=True)

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
    """

    name = models.CharField(
        _("Имя"),
        max_length=40,
        help_text=_("Имя поля модели"),
    )
    product = models.ForeignKey(
        ContentType,
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
                    _("Опция с данным именем переменной не является числовой опцией.")
                )
        if self.product is not None:
            products = Product.objects.filter(
                polymorphic_ctype=self.product
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
        help_text=_("Имя переменной для формулы"),
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Связать с ценой из прайс листа"),
    )
    variability_with_block_amount = models.BooleanField(
        _("Изменяется вместе с кол-вом в блоке"),
        default=False,
        help_text=_("Нельзя использовать вместе с категорией продукции"),
    )
    initial_value = models.IntegerField(
        _("Начальное числовое значение"),
        blank=True,
        null=True,
        help_text=_(
            "Можно оставить пустым для 1 (при условии, что выбрана изменяемость)"
        ),
    )

    class Meta:
        verbose_name = "Опция со значением"
        verbose_name_plural = "Опции со значениями"

    def clean(self) -> None:
        super().clean()
        if self.variability_with_block_amount and self.option_type not in (
            "counter",
            "number",
        ):
            raise ValidationError(
                _("Изменяемость работает только с числовыми опциями.")
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# class BlockOption(models.Model):
#     """
#     Модель опции для блока калькулятора.

#     Атрибуты:
#         block (ForeignKey): Ссылка на блок калькулятора.
#         position (int): Позиция опции в списке.
#         title (str): Название опции.
#         description (str): Описание опции.
#         option_type (str): Тип опции (число, выбор, подтверждение, счетчик).
#         name (str): Имя переменной для формулы или имя поля модели.
#         choices (str): Варианты выбора для опции.
#         product (str): Название категории для фильтрации.
#         filters (str): Фильтры для товара.
#         depends_on (ForeignKey): Ссылка на опцию, от которой зависит текущая опция.
#         depends_on_value (str): Значение, от которого зависит текущая опция.
#         price (ForeignKey): Ссылка на цену.
#         block_amount_undependent (bool): Флаг независимости кол-ва товара для опции от кол-ва в самом блоке.
#         amount_depend (str): Название переменной в которой содержится кол-во для товара.
#     """

#     class OptionTypes(models.TextChoices):
#         NUMBER = ("number", _("Число"))
#         RADIO = ("radio", _("Выбор"))
#         CHECKBOX = ("checkbox", _("Подтверждение"))
#         COUNTER = ("counter", _("Счетчик"))

#     block = models.ForeignKey(
#         CalculatorBlock, on_delete=models.CASCADE, related_name="options"
#     )
#     position = models.IntegerField(
#         _("Позиция в списке"),
#         validators=[MinValueValidator(1)],
#     )
#     title = models.CharField(_("Название"), max_length=40)
#     description = models.CharField(_("Описание"))
#     option_type = models.CharField(_("Тип опции"), choices=OptionTypes.choices)
#     name = models.CharField(
#         _("Имя"),
#         max_length=40,
#         help_text=_("Имя переменной для формулы или имя поля модели"),
#     )
#     choices = models.CharField(
#         _("Выбор"), blank=True, null=True, help_text=_("Перечислите варианты через ';'")
#     )
#     depends_on = models.ForeignKey(
#         "BlockOption",
#         on_delete=models.SET_NULL,
#         verbose_name=_("Зависит от опции"),
#         blank=True,
#         null=True,
#         related_name="dependent",
#     )
#     depends_on_value = models.CharField(_("Зависит от значения опции"), blank=True)
#     product = models.ForeignKey(
#         ProductCategory,
#         on_delete=models.SET_NULL,
#         verbose_name=_("Категория товара для фильтрации"),
#         blank=True,
#         null=True,
#     )
#     filters = models.TextField(
#         _("Фильтры для товара"),
#         blank=True,
#         null=True,
#         help_text=_(
#             "Фильтры перечисленые через запятую.\n"
#             "Доступные операторы:\n"
#             "1. Равенство: ==.\n"
#             "2. Неравенство: !=.\n"
#             "3. Больше: >.\n"
#             "4. Меньше: <.\n"
#             "5. Больше или равно: >=.\n"
#             "6. Меньше или равно: <=.\n"
#             "Пример: type == HD, price <= 1000"
#         ),
#     )
#     block_amount_undependent = models.BooleanField(
#         _("Кол-во товара не зависит от кол-ва в самом блоке"),
#         default=False,
#         help_text=_("Не будет учитываться если нет связи с категорией продукции"),
#     )
#     amount_depend = models.CharField(
#         _("Кол-во товара зависит от переменной"),
#         blank=True,
#         null=True,
#         help_text=_("Название переменной другой опции из этого блока"),
#     )
#     price = models.ForeignKey(
#         Price,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         help_text=_("Связать с ценой из прайс листа"),
#     )
#     variability_with_block_amount = models.BooleanField(
#         _("Изменяется вместе с кол-вом в блоке"),
#         default=False,
#         help_text=_("Нельзя использовать вместе с категорией продукции"),
#     )
#     initial_value = models.IntegerField(
#         _("Начальное числовое значение"),
#         blank=True,
#         null=True,
#         help_text=_(
#             "Можно оставить пустым для 1 (при условии, что выбрана изменяемость)"
#         ),
#     )
#     created_at = models.DateTimeField(
#         _("Дата создания"), auto_now_add=True, blank=True, null=True
#     )
#     updated_at = models.DateTimeField(
#         _("Дата обновления"), auto_now=True, blank=True, null=True
#     )

#     class Meta:
#         ordering = ("position",)
#         verbose_name = _("Опция для блока")
#         verbose_name_plural = _("Опции блока")

#     def __str__(self) -> str:
#         return f"{self.block.calculator}-{self.block.title}. {self.title}"

#     def clean(self) -> None:
#         # TODO нужно ли???
#         # count = BlockOption.objects.filter(block=self.block).count()
#         # if self.pk is None:
#         #     count += 1
#         # if self.position > count:
#         #     raise ValidationError(
#         #         _("Позиция не должна превышать кол-во опций у блока.")
#         #     )
#         if self.product and self.variability_with_block_amount:
#             raise ValidationError(
#                 _("Нельзя назначить категорию товара и изменяемость одновременно.")
#             )
#         if self.variability_with_block_amount and self.option_type not in (
#             "counter",
#             "number",
#         ):
#             raise ValidationError(
#                 _("Изменяемость работает только с числовыми опциями.")
#             )
#         if self.block_amount_undependent and self.amount_depend:
#             option = BlockOption.objects.filter(
#                 block=self.block, name=self.amount_depend
#             ).first()
#             if option is None:
#                 raise ValidationError(
#                     _("В блоке нет опции с данным именем переменной.")
#                 )
#             if option.option_type not in ("number", "counter"):
#                 raise ValidationError(
#                     _("Опция с данным именем переменной не является числовой опцией.")
#                 )
#         if self.price and self.product:
#             raise ValidationError(
#                 _(
#                     "Нельзя связать с категорией товара и ценой из прайс листа одновременно."
#                 )
#             )
#         if self.depends_on is not None:
#             if self.depends_on.pk == self.pk:
#                 raise ValidationError(
#                     _("Нельзя сделать опцию зависимой от самой себя.")
#                 )
#             if self.depends_on.block != self.block:
#                 raise ValidationError(
#                     _("Опция, от которой зависим, должна быть из текущего блока.")
#                 )
#         if self.product is not None:
#             products = Product.objects.filter(
#                 category__title=self.product
#             ).get_real_instances()
#             found = False
#             for product in products:
#                 if self.name in map(
#                     lambda x: x.attname, product._meta._get_fields(reverse=False)
#                 ):
#                     found = True
#                     break
#             if not found:
#                 raise ValidationError(
#                     _("Такого поля у данной категории моделей не существует")
#                 )

#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)
