from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"
    verbose_name = "Товар"

    def ready(self) -> None:
        import product.signals  # noqa: F401
