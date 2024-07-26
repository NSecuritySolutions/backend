from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from calculator.models import Price, PriceListCategory


@receiver(post_save, sender=Price)
@receiver(post_delete, sender=Price)
def update_pricelist_date(sender, instance: Price, **kwargs):
    if instance.price_list_category and instance.price_list_category.price_list:
        price_list = instance.price_list_category.price_list
        price_list.date = timezone.now()
        price_list.save()


@receiver(post_save, sender=PriceListCategory)
@receiver(post_delete, sender=PriceListCategory)
def update_pricelist_date_category(sender, instance: PriceListCategory, **kwargs):
    price_list = instance.price_list
    if price_list and Price.objects.filter(price_list_category=instance).exists():
        price_list.date = timezone.now()
        price_list.save()
