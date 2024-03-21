from django.core.management.base import BaseCommand
from product.models import Product
import requests
import schedule
import time

class Command(BaseCommand):
    help = 'Parse data from API and update prices in the database every 24 hours'

    def handle(self, *args, **kwargs):
        # schedule.every(24).hours.do(self.update_prices) 
        schedule.every(10).seconds.do(self.update_prices) #Закоментировать тест строку
        
        while True:
            schedule.run_pending()
            time.sleep(1)

    def update_prices(self):
        products = Product.objects.all()
        for product in products:
            try:
                response = requests.get(f'https://b2b.pro-tek.pro/api/v1/product?filters%5Bkeyword%5D=Аналог%3A{product.article}')
                # response = (f'https://b2b.pro-tek.pro/api/v1/product?filters%5Bkeyword%5D=Аналог%{url_article}')
                if response.status_code == 200:
                    data = response.json()
                    price = self.extract_price(data)
                    if price is not None:
                        product_instance, created = Product.objects.get_or_create(
                            article=product.article,
                            defaults={'price': price}  # Обновляем цену, если объект существует
                        )
                        if not created:  # Если объект уже существует, обновляем цену
                            product_instance.price = price
                            product_instance.save()
            except Exception as e:
                print(f"Error updating price for product {product.model}: {str(e)}")

    def extract_price(self, data):
        try:
            # Здесь необходимо написать код для извлечения цены из JSON-данных
            # Например, если цена находится в ключе "price" внутри "items", код может выглядеть так:
            price = data['items'][0]['price']['value']
            return price
        except Exception as e:
            print("Error extracting price from JSON:", str(e))
            return None
