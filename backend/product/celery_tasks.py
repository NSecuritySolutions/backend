import requests
from celery import shared_task
from django.core.files.base import ContentFile

from product.models import NewProduct


@shared_task
def download_and_save_image(product_id: int, image_url: str) -> None:
    """Загружает изображение по URL и сохраняет его в модель."""
    response = requests.get(f"https://b2b.pro-tek.pro{image_url}")
    if response.status_code == 200:
        product = NewProduct.objects.get(id=product_id)
        filename = f"{product_id}.jpg"
        product.image.save(filename, ContentFile(response.content), save=True)


@shared_task
def update_prices() -> bool:
    """Обновление цен всех товаров с артикулом."""
    queryset = NewProduct.objects.all()
    for instance in queryset:
        if instance.article is None:
            continue
        response = requests.get(
            f"https://b2b.pro-tek.pro/api/v1/product?filters[keyword]=Аналог:{instance.article}"
        )
        json = response.json()
        for item in json["items"]:
            if item.get("article", None) == instance.article:
                if (price := item.get("price", None)) is not None:
                    if (price_value := price.get("value", None)) is not None:
                        instance.price = price_value
                if not instance.image:
                    if (images := item.get("image", None)) is not None:
                        if images.get("750", None) is not None:
                            image_url = images.get("750")
                            download_and_save_image.delay(instance.pk, image_url)
                instance.save()
                continue
    # на bulk запросы не реагируют методы модели (save и др.) и сигналы
    # instances.bulk_update(queryset, ["price"])
    return True
