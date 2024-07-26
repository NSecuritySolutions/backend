from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import Product


@receiver(post_save, sender=Product)
def update_pricelist_date(sender, instance: Product, **kwargs):
    for price in instance.prices_in_price_lists:
        price.price = instance.price
        price.save()
