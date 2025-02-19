import requests
from celery import shared_task

from product.models import FACP, Camera, OtherProduct, Product, Register, Sensor


@shared_task
def update_prices() -> bool:
    instances = Product.objects.all()
    queryset: list[Camera | Register | OtherProduct | FACP | Sensor] = (
        instances.get_real_instances()
    )
    for instance in queryset:
        if instance.article is None:
            continue
        response = requests.get(
            f"https://b2b.pro-tek.pro/api/v1/product?filters[keyword]={instance.article}"
        )
        json = response.json()
        for item in json["items"]:
            if item["article"] == instance.article:
                instance.price = item["price"]["value"]
                instance.save()
    # на bulk запросы не реагируют методы модели (save и др.) и сигналы
    # instances.bulk_update(queryset, ["price"])
    return True
