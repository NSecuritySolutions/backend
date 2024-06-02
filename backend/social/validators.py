from django.core.exceptions import ValidationError


def validate_telegram_url(value: str):
    if not value.startswith("https://t.me/"):
        raise ValidationError("Ссылка должна начинаться с 'https://t.me/'")


def validate_whatsapp_url(value: str):
    urls = ["whatsapp://send?", "https://wa.me/", "https://chat.whatsapp.com/"]
    if not any(value.startswith(url) for url in urls):
        raise ValidationError("Не похоже на ссылку whatsapp")
