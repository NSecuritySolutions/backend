from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Дата создания"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"), auto_now=True, blank=True, null=True
    )

    class Meta:
        abstract = True


class Application(PolymorphicModel, BaseModel):
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
    calculator_data = models.JSONField(verbose_name=_("Данные из калькулятора"))

    class Meta:
        verbose_name = "Завка с калькулятором"
        verbose_name_plural = "Заявки с калькулятором"


class TelegramChat(BaseModel):
    chat_id = models.IntegerField(
        verbose_name=_("ID чата пользователя"), unique=True, db_index=True
    )
    send_application = models.BooleanField(
        verbose_name=_("Уведомлять о заявках"), default=False
    )

    class Meta:
        verbose_name = "Телеграм чат"
        verbose_name_plural = "Телеграм чаты"
