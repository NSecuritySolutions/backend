from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from polymorphic.models import PolymorphicModel

from product.validators import validate_field_name


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Дата создания"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"), auto_now=True, blank=True, null=True
    )

    class Meta:
        abstract = True


class ProductCategory(MPTTModel, BaseModel):
    """
    Модель категории товара.

    Атрибуты:
        title (str): Название категории товара.
    """

    title = models.CharField(verbose_name=_("Название"), max_length=50, unique=True)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name = _("Категория продукции")
        verbose_name_plural = _("Категории продукции")

    def __str__(self):
        return f"{self.title}"


class Tag(BaseModel):
    """
    Модель тэга.

    Атрибуты:
        title (str): Название тэга.
    """

    title = models.CharField(verbose_name=_("Название"), max_length=50)

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")

    def __str__(self) -> str:
        return f"{self.title}"


class Manufacturer(BaseModel):
    """
    Модель производителя.

    Атрибуты:
        title (str): Название производителя.
    """

    title = models.CharField(verbose_name=_("Название"), max_length=50)

    class Meta:
        verbose_name = _("Производитель")
        verbose_name_plural = _("Производители")

    def __str__(self) -> str:
        return f"{self.title}"


class Product(PolymorphicModel, BaseModel):
    """
    Модель товара с общими для всех товаров атрибутами.

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
    """

    article = models.CharField(verbose_name=_("Артикул"), max_length=100, blank=True)
    model = models.CharField(
        verbose_name=_("Модель"), max_length=300, help_text=_("Название поля: model")
    )
    image = models.ImageField(verbose_name=_("Изображение"), upload_to="media/product")
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Производитель"),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    price = models.IntegerField(
        verbose_name=_("Цена"),
        default=0,
        help_text=_("Название поля: price"),
        validators=[MinValueValidator(0)],
    )
    tooltip = models.TextField(
        verbose_name=_("Информация в тултипе"), max_length=200, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Товары")
        verbose_name_plural = _("Товары")

    def __str__(self) -> str:
        return self.model


class Camera(Product):
    """
    Модель камеры.

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
        type (str): Тип камеры.
        form_factor (str): Форм-фактор камеры.
        accommodation (str): Размещение камеры.
        resolution (str): Разрешение камеры.
        resolution_type (str): Тип разрешения камеры.
        dark (str): Съемка в темноте.
        temperature (str): Рабочая температура камеры.
        power_supply (str): Электропитание камеры.
        microphone (bool): Наличие микрофона.
        microphone_details (str): Подробности для микрофона.
        micro_sd (bool): Поддержка MicroSD.
        micro_sd_details (str): Подробности для MicroSD.
        viewing_angle (str): Угол обзора камеры.
        focus (str): Фокус камеры.
    """

    type = models.CharField(
        verbose_name=_("Тип"), max_length=20, help_text=_("Название поля: type")
    )
    form_factor = models.CharField(
        verbose_name=_("Форм Фактор"),
        max_length=50,
        help_text=_("Название поля: form_factor"),
    )
    accommodation = models.CharField(
        verbose_name=_("Размещение"),
        max_length=50,
        help_text=_("Название поля: accommodation"),
    )
    resolution = models.CharField(
        verbose_name=_("Разрешение"),
        max_length=50,
        help_text=_("Название поля: resolution"),
    )
    resolution_type = models.CharField(
        verbose_name=_("Тип разрешения"),
        max_length=30,
        help_text=_("Название поля: resolution_type"),
        blank=True,
    )
    dark = models.CharField(
        verbose_name=_("Съемка в темноте"),
        max_length=30,
        help_text=_("Название поля: dark"),
    )
    temperature = models.CharField(
        verbose_name=_("Рабочая температура"),
        max_length=30,
        help_text=_("Название поля: temperature"),
    )
    power_supply = models.CharField(
        verbose_name=_("Электропитание"),
        max_length=30,
        help_text=_("Название поля: power_supply"),
    )
    microphone = models.BooleanField(
        verbose_name=_("Наличичие микрофона"),
        max_length=30,
        default=False,
        help_text=_("Название поля: microphone"),
    )
    microphone_details = models.TextField(
        verbose_name=_("Подробности для микрофона"),
        help_text=_("Название поля: microphone_details"),
        blank=True,
    )
    micro_sd = models.BooleanField(
        verbose_name=_("Поддержка MicroSD"),
        max_length=30,
        help_text=_("Название поля: micro_sd"),
        default=False,
    )
    micro_sd_details = models.TextField(
        _("Подробности для MicroSD"),
        help_text=_("Название поля: micro_sd_details"),
        blank=True,
    )
    viewing_angle = models.CharField(
        verbose_name=_("Угол Обзора"),
        max_length=50,
        help_text=_("Название поля: viewing_angle"),
    )
    focus = models.CharField(
        verbose_name=_("Фокус"), max_length=50, help_text=_("Название поля: focus")
    )

    class Meta:
        verbose_name = _("Камера")
        verbose_name_plural = _("Камеры")

    def __str__(self) -> str:
        return self.model


class Register(Product):
    """
    Модель регистратора.

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
        max_resolution (str): Максимальное разрешение.
        quantity_cam (int): Количество камер.
        quantity_hdd (int): Количество HDD.
        max_size_hdd (int): Максимальный объем HDD в Тб.
        power_supply (str): Электропитание регистратора.
    """

    max_resolution = models.CharField(
        verbose_name=_("Максимально разрешение"),
        max_length=50,
        help_text=_("Название поля: max_resolution"),
    )
    quantity_cam = models.IntegerField(
        verbose_name=_("Количество камер"),
        help_text=_("Название поля: quantity_cam"),
        validators=[MinValueValidator(0)],
    )
    quantity_hdd = models.IntegerField(
        verbose_name=_("Количество HDD"),
        help_text=_("Название поля: quantity_hdd"),
        validators=[MinValueValidator(0)],
    )
    max_size_hdd = models.IntegerField(
        verbose_name=_("Макс объем HDD Тб"),
        help_text=_("Название поля: max_size_hdd"),
        validators=[MinValueValidator(0)],
    )
    type = models.CharField(
        verbose_name=_("Тип"),
        max_length=50,
        help_text=_("Название поля: type"),
    )
    power_supply = models.CharField(
        verbose_name=_("Электропитание"),
        max_length=50,
        help_text=_("Название поля: power_supply"),
    )

    class Meta:
        verbose_name = _("Регистраторы")
        verbose_name_plural = _("Регистраторы")

    def __str__(self) -> str:
        return self.model


class HDD(Product):
    """
    Модель жёсткого диска.

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
        capacity (int): Ёмкость.
    """

    capacity = models.IntegerField(
        _("Ёмкость, tb"),
        validators=[MinValueValidator(1)],
        help_text=_("Название поля: capacity"),
    )

    class Meta:
        verbose_name = "Жёсткий диск"
        verbose_name_plural = "Жёсткие диски"

    def __str__(self) -> str:
        return f"{self.model}"


class FACP(Product):
    """
    Модель ППКОП (прибор приемно-контрольный охранно-пожарный).

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
        alarm_loops (int): Количество шлейфов сигнализации.
        wireless_sensor_support (bool): Поддержка беспроводных извещателей.
        phone_control (bool): Управление с телефона.
        temperature (str): Рабочая температура.
    """

    alarm_loops = models.IntegerField(
        verbose_name=_("Кол-во шлейфов сигнализации"),
        validators=[MinValueValidator(0)],
        help_text=_("Название поля: alarm_loops"),
    )
    wireless_sensor_support = models.BooleanField(
        verbose_name=_("Поддержка беспроводных извещателей"),
        default=False,
        help_text=_("Название поля: wireless_sensor_support"),
    )
    phone_control = models.BooleanField(
        verbose_name=_("Управление с телефона"),
        default=False,
        help_text=_("Название поля: phone_control"),
    )
    temperature = models.CharField(
        verbose_name=_("Рабочая температура"),
        max_length=30,
        help_text=_("Название поля: temperature"),
    )

    class Meta:
        verbose_name = "ППКОП"
        verbose_name_plural = "ППКОПы"

    def __str__(self) -> str:
        return f"{self.model}"


class Sensor(Product):
    """
    Модель извещателя.

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
        temperature (str): Рабочая температура извещателя.
    """

    temperature = models.CharField(
        verbose_name=_("Рабочая температура"),
        max_length=30,
        help_text=_("Название поля: temperature"),
    )

    class Meta:
        verbose_name = "Извещатель"
        verbose_name_plural = "Извещатели"

    def __str__(self) -> str:
        return f"{self.model}"


class OtherProduct(Product):
    """
    Модель остального товара.

    Атрибуты:
        article (str): Артикул товара.
        model (str): Модель товара.
        image (ImageField): Изображение товара.
        description (str): Описание товара.
        manufacturer (ForeignKey): Производитель товара.
        category (ForeignKey): Категория товара.
        price (int): Цена товара.
    """

    class Meta:
        verbose_name = "Остальной товар"
        verbose_name_plural = "Остальные товары"

    def __str__(self) -> str:
        return f"{self.model}"


class ReadySolution(BaseModel):
    """
    Модель готового решения.

    Атрибуты:
        title (str): Название решения.
        image (ImageField): Фотография решения.
        tooltip_text (str): Подсказка.
        description (str): Описание решения.
        price (int): Цена решения.
        tags (ManyToManyField): Тэги решения.
    """

    title = models.CharField(verbose_name=_("Название"), max_length=300)
    image = models.ImageField(verbose_name=_("Фотография"), upload_to="media/ready")
    tooltip_text = models.TextField(verbose_name=_("Подсказка"), max_length=1000)
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    price = models.DecimalField(
        verbose_name=_("Корректировка цены"),
        help_text=_(
            "Дополнительная сумма к цене оборудования. Может быть отрицательной для скидки."
        ),
        default=Decimal(0),
        max_digits=12,
        decimal_places=2,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("Тэги"))

    class Meta:
        verbose_name = _("Готовые решение")
        verbose_name_plural = _("Готовые решения")

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = Decimal(0)
        super().save(*args, **kwargs)


class SolutionToProduct(BaseModel):
    """
    Промежуточная модель между готовым решением и продукцией.

    Атрибуты:
        solution (ForeignKey): Ссылка на готовое решение.
        text (str): Краткое описание товара.
        is_link (bool): Флаг, указывающий, отображать ли текст как ссылку на товар.
        product (ForeignKey): Ссылка на товар.
        calculator_block (ForeignKey): Ссылка на блок в калькуляторе.
        amount (int): Количество товара в решении.
    """

    solution = models.ForeignKey(
        ReadySolution, on_delete=models.CASCADE, related_name="equipment"
    )
    position = models.IntegerField(
        _("Позиция в списке"), validators=[MinValueValidator(0)], null=True, blank=True
    )
    text = models.CharField(_("Текст"), max_length=200, help_text=_("Краткое описание"))
    is_link = models.BooleanField(
        _("Ссылка"), default=False, help_text=_("Отобразить как ссылку на товар")
    )
    product = models.ForeignKey(
        "NewProduct", on_delete=models.SET_NULL, blank=True, null=True
    )
    calculator_block = models.ForeignKey(
        "calculator.CalculatorBlock", on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.IntegerField(
        _("Кол-во"), validators=[MinValueValidator(1)], blank=True, null=True
    )
    show = models.BooleanField(_("Отобразить на сайте"), default=True)

    class Meta:
        ordering = ("position", "pk")
        verbose_name = _("Товар к готовому решению")
        verbose_name_plural = _("Товары к готовым решениям")


class OurService(BaseModel):
    """
    Модель наших услуг.

    Атрибуты:
        image (ImageField): Фотография услуги.
        title (str): Название услуги.
        description (str): Описание услуги.
        action (str): Текст кнопки действия.
    """

    image = models.ImageField(verbose_name=_("Фотография"), upload_to="media/service")
    title = models.CharField(verbose_name=_("Название"), max_length=400)
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    action = models.CharField(
        verbose_name=_("Текст кнопки"), max_length=20, default="Подробнее"
    )

    class Meta:
        verbose_name = _("Наши услуги")
        verbose_name_plural = _("Наши услуги")

    def __str__(self) -> str:
        return f"{self.title}"


class ImageWorks(BaseModel):
    """
    Модель картинки для примера работы.

    Атрибуты:
        work (ForeignKey): Ссылка на пример работы.
        image (ImageField): Фотография.
        is_main (bool): Флаг, указывающий, является ли изображение основным.
    """

    work = models.ForeignKey(
        "OurWorks", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(verbose_name=_("Фотографии"), upload_to="media/our_works")
    is_main = models.BooleanField(_("Картинка на главной"))

    class Meta:
        verbose_name = _("Фотографии")
        verbose_name_plural = _("Фотографии")

    def __str__(self) -> str:
        return f"Image {self.image}"

    def clean(self) -> None:
        count = ImageWorks.objects.filter(work=self.work).count()
        if count > 5:
            raise ValidationError(_("Разрешено не более 5 картинок."))
        if self.is_main:
            prev_main_image = ImageWorks.objects.filter(
                ~models.Q(pk=self.pk), is_main=True, work=self.work
            )
            if prev_main_image:
                raise ValidationError(_("Только одна картинка может быть на главной."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class OurWorks(BaseModel):
    """
    Модель примера работ.

    Атрибуты:
        title (str): Название работы.
        product (str): Используемое оборудование.
        description (str): Описание работы.
        add_date (datetime): Дата добавления работы на сайт.
        time (int): Затраченное время.
        budget (int): Бюджет работы.
        area (int): Площадь работ.
        is_active (bool): Флаг, указывающий, находится ли работа на главной странице.
    """

    title = models.CharField(verbose_name=_("Название"), max_length=300)
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    add_date = models.DateTimeField(verbose_name=_("Дата добавления на сайт"))
    time = models.IntegerField(
        verbose_name=_("Затраченное время"), validators=[MinValueValidator(1)]
    )
    budget = models.DecimalField(
        verbose_name=_("Бюджет"),
        validators=[MinValueValidator(Decimal(0))],
        max_digits=12,
        decimal_places=2,
    )
    area = models.IntegerField(
        verbose_name=_("Площадь работ"), validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(verbose_name=_("На главной"), default=False)

    class Meta:
        verbose_name = _("Примеры работ")
        verbose_name_plural = _("Примеры работ")

    def __str__(self) -> str:
        return self.title


class OurWorksProduct(BaseModel):
    """
    Промежуточная модель для связи наших работ с товаром.

    Атрибуты:
        our_work (ForeignKey): Работа.
        text (str): Краткое описание товара.
        is_link (bool): Флаг, указывающий, отображать ли текст как ссылку на товар.
        product (ForeignKey): Товар.
        amount (int): Кол-во товара, используемого в работе.
    """

    our_work = models.ForeignKey(
        OurWorks, on_delete=models.CASCADE, related_name="products"
    )
    text = models.CharField(_("Текст"), max_length=200, help_text=_("Краткое описание"))
    is_link = models.BooleanField(
        _("Ссылка"), default=False, help_text=_("Отобразить как ссылку на товар")
    )
    product = models.ForeignKey(
        "NewProduct", on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.IntegerField(
        _("Кол-во"), validators=[MinValueValidator(1)], blank=True, null=True
    )

    class Meta:
        verbose_name = _("Использованный товар")
        verbose_name_plural = _("Использованные товары")


class TypeProperty(BaseModel):
    field_name = models.CharField(
        _("Название поля характеристики"), validators=(validate_field_name,)
    )
    name = models.CharField(_("Название характеристики"))
    property_type = models.CharField(
        _("Тип характеристики"),
        max_length=10,
        choices=[
            ("text", "Текст"),
            ("integer", "Целое число"),
            ("float", "Десятичное число"),
            ("boolean", "Логический тип"),
        ],
        default="text",
    )

    class Meta:
        verbose_name = _("Хар-ка")
        verbose_name_plural = _("Хар-ки")

    def __str__(self):
        return f"{self.name} ({self.property_type})"


class ProductType(BaseModel):
    name = models.CharField(_("Название"))
    properties = models.ManyToManyField(
        TypeProperty, related_name="product_types", through="ProductTypeTypeProperty"
    )

    class Meta:
        verbose_name = _("Вид товара")
        verbose_name_plural = _("Виды товаров")

    def __str__(self):
        return f"{self.pk} - {self.name}"

    def clear_unusable_props(self):
        with transaction.atomic():
            for prop_for_delete in ProductProperty.objects.filter(
                product__in=NewProduct.objects.filter(product_type=self.pk),
            ).exclude(property__in=self.properties.all()):
                prop_for_delete.delete()


class ProductTypeTypeProperty(BaseModel):
    producttype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    typeproperty = models.ForeignKey(TypeProperty, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Хар-ка вида товара")
        verbose_name_plural = _("Хар-ки видов товаров")

    def __str__(self):
        return f"{self.producttype.name} - {self.typeproperty.name}"

    def clean(self) -> None:
        super().clean()
        count_unique = (
            ProductTypeTypeProperty.objects.exclude(pk=self.pk)
            .filter(
                typeproperty__field_name=self.typeproperty.field_name,
                producttype=self.producttype,
            )
            .count()
        )
        if count_unique > 0:
            raise ValidationError(
                "Поле 'field_name' у характеристики должно быть уникальным в рамках одного вида товара."
            )

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        with transaction.atomic():
            for product in NewProduct.objects.filter(product_type=self.producttype):
                ProductProperty.objects.get_or_create(
                    product=product,
                    property=self.typeproperty,
                    defaults={"value": None},
                )
            self.producttype.clear_unusable_props()

    def delete(self, *args, **kwargs) -> None:
        super().delete(*args, **kwargs)
        with transaction.atomic():
            for product in NewProduct.objects.filter(product_type=self.producttype):
                product_property = ProductProperty.objects.filter(
                    product=product, property=self.typeproperty
                ).first()
                if product_property:
                    product_property.delete()


class NewProduct(BaseModel):
    product_type = models.ForeignKey(
        ProductType,
        verbose_name=_("Вид товара"),
        on_delete=models.CASCADE,
        related_name="products",
    )
    article = models.CharField(
        verbose_name=_("Артикул"), max_length=100, blank=True, null=True
    )
    model = models.CharField(verbose_name=_("Модель"), max_length=300)
    image = models.ImageField(
        verbose_name=_("Изображение"), upload_to="media/product", blank=True, null=True
    )
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Производитель"),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        verbose_name=_("Цена"),
        default=Decimal(0),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0))],
    )
    tooltip = models.TextField(
        verbose_name=_("Информация в тултипе"), max_length=200, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self) -> str:
        return self.model

    def save(self, *args, **kwargs):
        is_product_type_changed = False
        if self.pk:
            old_product_type = (
                NewProduct.objects.filter(pk=self.pk).values("product_type").first()
            )
            if (
                old_product_type
                and old_product_type["product_type"] != self.product_type_id
            ):
                is_product_type_changed = True

        if is_product_type_changed:
            new_type_property_ids = set(
                self.product_type.properties.values_list("id", flat=True)
            )
            ProductProperty.objects.filter(product=self).exclude(
                property_id__in=new_type_property_ids
            ).delete()

        super().save(*args, **kwargs)

        for property in self.product_type.properties.all():
            ProductProperty.objects.get_or_create(
                product=self, property=property, defaults={"value": None}
            )


class ProductProperty(BaseModel):
    product = models.ForeignKey(
        NewProduct, on_delete=models.CASCADE, related_name="properties"
    )
    property = models.ForeignKey(TypeProperty, on_delete=models.CASCADE)
    value = models.CharField(null=True, blank=True)

    class Meta:
        ordering = ("property",)
        verbose_name = _("Хар-ка товара")
        verbose_name_plural = _("Хар-ки товаров")

    def __str__(self):
        return f"{self.property.name}: {self.value}"

    def get_typed_value(self):
        if self.property.property_type == "integer":
            return int(self.value) if self.value is not None else None
        elif self.property.property_type == "float":
            return Decimal(self.value) if self.value is not None else None
        elif self.property.property_type == "boolean":
            return (
                self.value.lower() in ("true", "false")
                if self.value is not None
                else None
            )
        return self.value

    def clean(self) -> None:
        # if self.property not in self.product.product_type.properties.all():
        #     raise ValidationError(
        #         f"Атрибут '{self.property.name}' не разрешён для типа товара '{self.product.product_type.name}'."
        #     )
        if self.value is not None:
            if self.property.property_type == "integer":
                if not self.value.isdigit():
                    raise ValidationError(
                        f"Значение '{self.value}' не является целым числом для характеристики '{self.property.name}'."
                    )
            elif self.property.property_type == "float":
                try:
                    Decimal(self.value)
                except (ValueError, TypeError):
                    raise ValidationError(
                        f"Значение '{self.value}' не является десятичным числом для характеристики '{self.property.name}'."
                    )
            elif self.property.property_type == "boolean":
                if self.value.lower() not in ("true", "false"):
                    raise ValidationError(
                        f"Значение '{self.value}' не является логическим для характеристики '{self.property.name}'."
                    )
        return super().clean()
