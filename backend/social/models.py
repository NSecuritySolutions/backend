from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class QuestionsCategory(models.Model):
    """Модель категории для вопросов."""

    name = models.CharField(_("Название"), max_length=100)

    class Meta:
        verbose_name = _("Категория вопросов")
        verbose_name_plural = _("Категории вопросов")

    def __str__(self) -> str:
        return self.name


class Questions(models.Model):
    """Модель вопроса."""

    question = models.CharField(verbose_name=_("Вопрос"), max_length=200)
    answer = models.TextField(verbose_name=_("Ответ"), max_length=500)
    category = models.ForeignKey(
        QuestionsCategory, verbose_name=_("Категория"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Вопрос/Ответ")
        verbose_name_plural = _("Вопрос/Ответ")

    def __str__(self) -> str:
        return f"{self.question}"


class Team(models.Model):
    """Модель команды."""

    description = models.TextField(_("Описание"), max_length=2000)


class Employee(models.Model):
    """Модель работника."""

    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, related_name="employees", null=True
    )
    image = models.ImageField(_("Фото"), upload_to=("media/team"))
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    position = models.CharField(_("Должность"), max_length=300)
    phone = PhoneNumberField(
        verbose_name=_("Номер телефона"),
        max_length=20,
        blank=False,
        unique=True,
    )
