from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel


class ProductCategory(models.Model):
    """Модель категории товара."""

    title = models.CharField(verbose_name=_("Название"), max_length=50)

    class Meta:
        verbose_name = _("Категория продукции")
        verbose_name_plural = _("Категории продукции")

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    """Модель тэга."""

    title = models.CharField(verbose_name=_("Название"), max_length=50)

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")

    def __str__(self) -> str:
        return f"{self.title}"


class Manufacturer(models.Model):
    """Модель производителя."""

    title = models.CharField(verbose_name=_("Название"), max_length=50)

    class Meta:
        verbose_name = _("Производитель")
        verbose_name_plural = _("Производители")

    def __str__(self) -> str:
        return f"{self.title}"


class Product(PolymorphicModel):
    """Модель товара с общими для всех товаров атрибутами."""

    article = models.CharField(verbose_name=_("Артикул"), max_length=100)
    model = models.CharField(verbose_name=_("Модель"), max_length=300)
    image = models.ImageField(verbose_name=_("Изображение"), upload_to="media/product")
    description = models.CharField(verbose_name=_("Описание"), max_length=5000)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name=_("Производитель"), on_delete=models.CASCADE
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

    class Meta:
        verbose_name = _("Товары")
        verbose_name_plural = _("Товары")

    def __str__(self) -> str:
        return self.model


class Camera(Product):
    """Модель камеры."""

    type = models.CharField(
        verbose_name=_("Тип"), max_length=20, help_text=_("Название поля: type")
    )
    form_factor = models.CharField(
        verbose_name=_("Форм Фактор"),
        max_length=20,
        help_text=_("Название поля: form_factor"),
    )
    accommodation = models.CharField(
        verbose_name=_("Размещение"),
        max_length=30,
        help_text=_("Название поля: accommodation"),
    )
    resolution = models.CharField(
        verbose_name=_("Разрешение"),
        max_length=30,
        help_text=_("Название поля: resolution"),
    )
    dark = models.CharField(
        verbose_name=_("Съемка в темноте"),
        max_length=30,
        help_text=_("Название поля: dark"),
    )
    temperature = models.CharField(
        verbose_name=_("Температура"),
        max_length=30,
        help_text=_("Название поля: temperature"),
    )
    power_supply = models.CharField(
        verbose_name=_("Электропитание"),
        max_length=30,
        help_text=_("Название поля: power_supply"),
    )
    microphone = models.CharField(
        verbose_name=_("Микрофон"),
        max_length=30,
        help_text=_("Название поля: microphone"),
    )
    micro_sd = models.CharField(
        verbose_name="MicroSD", max_length=30, help_text=_("Название поля: micro_sd")
    )
    viewing_angle = models.CharField(
        verbose_name=_("Угол Обзора"),
        max_length=30,
        help_text=_("Название поля: viewing_angle"),
    )
    focus = models.CharField(
        verbose_name=_("Фокус"), max_length=30, help_text=_("Название поля: focus")
    )

    class Meta:
        verbose_name = _("Камера")
        verbose_name_plural = _("Камеры")

    def __str__(self) -> str:
        return self.model


class Register(Product):
    """Модель регистратора."""

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


class HDD(models.Model):
    # TODO docstring
    model = models.CharField(verbose_name=_("Модель"), max_length=300)
    description = models.CharField(verbose_name=_("Описание"), max_length=5000)
    manufacturer = models.ManyToManyField(Manufacturer, verbose_name=_("Производитель"))
    price = models.IntegerField(
        verbose_name=_("Цена"), default=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "HDD"
        verbose_name_plural = "HDD"

    def __str__(self) -> str:
        return f"{self.model}"


class ReadySolution(models.Model):
    """Модель готового решения."""

    title = models.CharField(verbose_name=_("Название"), max_length=300)
    image = models.ImageField(verbose_name=_("Фотография"), upload_to="media/ready")
    tooltip_text = models.TextField(verbose_name=_("Подсказка"), max_length=200)
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    price = models.IntegerField(
        verbose_name=_("Цена"), null=True, blank=True, validators=[MinValueValidator(0)]
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("Тэги"))

    class Meta:
        verbose_name = _("Готовые решение")
        verbose_name_plural = _("Готовые решение")

    def __str__(self) -> str:
        return f"{self.title}"


class SolutionToProduct(models.Model):
    """Промежуточная модель между готовым решением и продукцией."""

    solution = models.ForeignKey(
        ReadySolution, on_delete=models.CASCADE, related_name="equipment"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(_("Кол-во"), validators=[MinValueValidator(1)])


class OurService(models.Model):
    """Модель наших услуг."""

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


class ImageWorks(models.Model):
    """Модель картинки для примера работы."""

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
        if self.is_main:
            prev_main_image = ImageWorks.objects.filter(
                ~models.Q(pk=self.pk), is_main=True, work=self.work
            )
            if prev_main_image:
                raise ValidationError(_("Только одна картинка может быть на главной."))


class OurWorks(models.Model):
    """Модель примера работ."""

    title = models.CharField(verbose_name=_("Название"), max_length=300)
    product = models.TextField(
        verbose_name=_("Используемое оборудование"), max_length=5000
    )
    description = models.TextField(verbose_name=_("Описание"), max_length=5000)
    add_date = models.DateTimeField(verbose_name=_("Дата добавления на сайт"))
    time = models.IntegerField(
        verbose_name=_("Затраченное время"), validators=[MinValueValidator(1)]
    )
    budget = models.IntegerField(
        verbose_name=_("Бюджет"), validators=[MinValueValidator(0)]
    )
    area = models.IntegerField(
        verbose_name=_("Площадь работ"), validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = _("Примеры работ")
        verbose_name_plural = _("Примеры работ")

    def __str__(self) -> str:
        return f"{self.title}"
