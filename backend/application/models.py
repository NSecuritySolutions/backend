from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel


class Application(PolymorphicModel):
    name = models.CharField(verbose_name=_("Имя"), max_length=50)
    email = models.EmailField(verbose_name=_("Почта"))
    phone = PhoneNumberField(
        verbose_name=_("Номер телефона"),
        max_length=20,
    )
    comment = models.TextField(
        verbose_name=_("Комментарий"), max_length=2000, null=True, blank=True
    )
    date = models.DateTimeField(_("Дата"), auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class ApplicationWithFile(Application):
    file = models.FileField(
        verbose_name=_("Приложенный файл"),
        upload_to="media/application",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Обычная заявка"
        verbose_name_plural = "Обычные заявки"


class ApplicationWithSolution(Application):
    solution = models.ForeignKey(
        "product.ReadySolution", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "Заявка на готовое решение"
        verbose_name_plural = "Заявки на готовое решение"


class ApplicationWithCalculator(Application):
    class Meta:
        verbose_name = "Завка с калькулятором"
        verbose_name_plural = "Заявки с калькулятором"


class CalculatorData(models.Model):
    application = models.OneToOneField(
        ApplicationWithCalculator, on_delete=models.CASCADE, related_name="calculator"
    )
    price = models.IntegerField(verbose_name=_("Общая стоимость"))


class CalculatorBlockData(models.Model):
    calculator_data = models.ForeignKey(
        CalculatorData, on_delete=models.CASCADE, related_name="blocks"
    )
    name = models.CharField(verbose_name=_("Название"))
    price = models.IntegerField(verbose_name=_("Стоимость"))
    amount = models.IntegerField(verbose_name=_("Кол-во"))


class CalculatorBlockCategoryProductsData(models.Model):
    block_data = models.ForeignKey(
        CalculatorBlockData, on_delete=models.CASCADE, related_name="products_category"
    )
    name = models.CharField(verbose_name=_("Название категории"))
    products = models.ManyToManyField(
        "product.Product", verbose_name=_("Подходящие товары"), blank=True
    )


class OptionData(models.Model):
    block_data = models.ForeignKey(
        CalculatorBlockData, on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(verbose_name=_("Название"))
    value = models.CharField(verbose_name=_("Значение"))
