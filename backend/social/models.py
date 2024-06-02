from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from social.validators import validate_telegram_url, validate_whatsapp_url


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
    is_active = models.BooleanField(verbose_name=_("Актуальная команда"), default=False)

    class Meta:
        verbose_name = _("Команда")
        verbose_name_plural = _("Команды")

    def __str__(self) -> str:
        return f"{self.pk}. {self.description}"

    def clean(self) -> None:
        if self.is_active:
            prev_active_calc = Team.objects.filter(
                ~models.Q(pk=self.pk), is_active=True
            )
            if prev_active_calc:
                raise ValidationError(_("Только одна команда может быть актуальной."))


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

    class Meta:
        verbose_name = _("Работник")
        verbose_name_plural = _("Работники")

    def __str__(self) -> str:
        return f"{self.first_name}. {self.last_name}"


class SocialInfo(models.Model):
    """Модель информации о компании."""

    phone = PhoneNumberField(
        verbose_name=_("Номер телефона"),
        max_length=20,
        blank=False,
    )
    email = models.EmailField(verbose_name=_("Почта для связи"))
    telegram = models.URLField(
        verbose_name=_("Ссылка на телеграм для связи"),
        validators=[validate_telegram_url],
    )
    whatsapp = models.URLField(
        verbose_name=_("Ссылка на whatsapp для связи"),
        validators=[validate_whatsapp_url],
    )
    address = models.CharField(verbose_name=_("Адресс"), max_length=500)
    years = models.IntegerField(
        verbose_name=_("Возраст компании"), validators=[MinValueValidator(0)]
    )
    projects_done = models.IntegerField(
        verbose_name=_("Кол-во завершенных проектов"), validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(
        verbose_name=_("Актуальная информация"), default=False
    )

    class Meta:
        verbose_name = _("Информация")
        verbose_name_plural = _("Информация")

    def __str__(self) -> str:
        return f"{self.pk}. {self.address}"

    def clean(self) -> None:
        if self.is_active:
            prev_active_calc = SocialInfo.objects.filter(
                ~models.Q(pk=self.pk), is_active=True
            )
            if prev_active_calc:
                raise ValidationError(
                    _("Только один социальный блок может быть актуальным.")
                )
