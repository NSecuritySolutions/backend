from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from social.validators import validate_telegram_url, validate_whatsapp_url


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Дата создания"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"), auto_now=True, blank=True, null=True
    )

    class Meta:
        abstract = True


class QuestionsCategory(BaseModel):
    """
    Модель категории для вопросов.

    Атрибуты:
        name (str): Название категории.
        icon (ImageField): Иконка категории.
    """

    name = models.CharField(_("Название"), max_length=100)
    icon = models.ImageField(_("Иконка категории"), upload_to="media/questions/icons")

    class Meta:
        verbose_name = _("Категория вопросов")
        verbose_name_plural = _("Категории вопросов")

    def __str__(self) -> str:
        return self.name


class Questions(BaseModel):
    """
    Модель вопроса.

    Атрибуты:
        question (str): Вопрос.
        answer (str): Ответ на вопрос.
        category (ForeignKey): Категория вопроса.
    """

    question = models.CharField(verbose_name=_("Вопрос"), max_length=200)
    answer = models.TextField(verbose_name=_("Ответ"), max_length=1000)
    category = models.ForeignKey(
        QuestionsCategory,
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
        related_name="questions",
    )

    class Meta:
        verbose_name = _("Вопрос/Ответ")
        verbose_name_plural = _("Вопрос/Ответ")

    def __str__(self) -> str:
        return f"{self.question}"


class Team(BaseModel):
    """
    Модель команды.

    Атрибуты:
        description (str): Описание команды.
        active (bool): Флаг, указывающий на актуальность команды.
    """

    description = models.TextField(_("Описание"), max_length=2000)
    active = models.BooleanField(verbose_name=_("Актуальная команда"), default=False)

    class Meta:
        verbose_name = _("Команда")
        verbose_name_plural = _("Команды")

    def __str__(self) -> str:
        return f"{self.pk}. {self.description}"

    def clean(self) -> None:
        if self.active:
            prev_active = Team.objects.filter(~models.Q(pk=self.pk), active=True)
            if prev_active:
                raise ValidationError(_("Только одна команда может быть актуальной."))


class Employee(BaseModel):
    """
    Модель работника.

    Атрибуты:
        team (ForeignKey): Ссылка на команду.
        image (ImageField): Фото работника.
        first_name (str): Имя работника.
        last_name (str): Фамилия работника.
        position (str): Должность работника.
        phone (PhoneNumberField): Номер телефона работника.
    """

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
        blank=True,
        unique=True,
    )

    class Meta:
        verbose_name = _("Работник")
        verbose_name_plural = _("Работники")

    def __str__(self) -> str:
        return f"{self.first_name}. {self.last_name}"


class SocialInfo(BaseModel):
    """
    Модель информации о компании.

    Атрибуты:
        phone (PhoneNumberField): Номер телефона компании.
        email (str): Почта для связи.
        telegram (URLField): Ссылка на телеграм для связи.
        whatsapp (URLField): Ссылка на WhatsApp для связи.
        address (str): Адрес компании.
        founded (DateField): Дата основания компании.
        projects_done (int): Количество завершенных проектов.
        active (bool): Флаг актуальности информации.
    """

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
    address = models.CharField(verbose_name=_("Адрес"), max_length=500)
    founded = models.DateField(verbose_name=_("Компания основана"), blank=False)
    projects_done = models.IntegerField(
        verbose_name=_("Кол-во завершенных проектов"), validators=[MinValueValidator(0)]
    )
    active = models.BooleanField(verbose_name=_("Актуальная информация"), default=False)

    class Meta:
        verbose_name = _("Информация")
        verbose_name_plural = _("Информация")

    def __str__(self) -> str:
        return f"{self.pk}. {self.address}"

    def clean(self) -> None:
        if self.active:
            prev_active = SocialInfo.objects.filter(~models.Q(pk=self.pk), active=True)
            if prev_active:
                raise ValidationError(
                    _("Только один социальный блок может быть актуальным.")
                )


class OurGuarantees(BaseModel):
    """
    Модель для 'мы обеспечиваем'.

    Атрибуты:
        icon (ImageField): Иконка гарантии.
        title (str): Название гарантии.
        is_big (bool): Флаг, указывающий на большую карточку.
        active (bool): Флаг, указывающий на отображение на главной странице.
    """

    icon = models.ImageField(verbose_name=_("Иконка"))
    title = models.CharField(verbose_name=_("Название"), max_length=30)
    is_big = models.BooleanField(verbose_name=_("Большая карточка"))
    active = models.BooleanField(verbose_name=_("На главной"))

    class Meta:
        verbose_name = _("Категория гарантий")
        verbose_name_plural = _("Категории гарантий")

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.active:
            prev_active = OurGuarantees.objects.filter(
                ~models.Q(pk=self.pk), active=True, is_big=False
            )
            if prev_active >= 4:
                raise ValidationError(
                    _("Только 4 обычные (по размеру) гарантии могут быть на главной.")
                )
            if self.is_big:
                prev_main = OurGuarantees.objects.filter(
                    ~models.Q(pk=self.pk), is_big=True, active=True
                )
                if prev_main:
                    raise ValidationError(
                        _("Только 1 категория гарантии может быть большой.")
                    )


class Subguarantees(BaseModel):
    """
    Модель подкатегорий гарантии.

    Атрибуты:
        guarantee (ForeignKey): Ссылка на категорию гарантии.
        text (str): Текст подкатегории.
    """

    guarantee = models.ForeignKey(
        OurGuarantees, on_delete=models.CASCADE, related_name="subguarantees"
    )
    text = models.CharField(verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Подкатегория гарантии")
        verbose_name_plural = _("Подкатегории гарантий")

    def __str__(self) -> str:
        return self.text

    def clean(self) -> None:
        subguarantees = Subguarantees.objects.filter(guarantee=self.guarantee)
        text_len = len(self.text)
        if len(subguarantees) >= 3:
            raise ValidationError(
                _("Подкатегорий гарантии не может быть больше 3 для одной категории.")
            )
        if (self.guarantee.is_big and text_len >= 90) or (
            not self.guarantee.is_big and text_len >= 60
        ):
            raise ValidationError(_("Недопустимая длина текста."))


class Reviews(BaseModel):
    name = models.CharField(verbose_name=_("Имя"), max_length=100)
    last_name = models.CharField(verbose_name=_("Фамилия"), max_length=100)
    title = models.CharField(verbose_name=_("Заголовок"), max_length=100)
    text = models.TextField(verbose_name=_("Текст"), max_length=2000)
    image = models.ImageField(
        verbose_name=_("Аватарка"), upload_to=("media/reviews"), blank=True, null=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}: {self.title}"
