import os

import requests
from celery import shared_task
from django.conf import settings

from application.models import TelegramChat
from product.models import ProductType, ReadySolution


def form_message_calculator_app(data: dict):
    price = data.get("price", None)
    blocks = data.get("blocks", None)
    string = f"<b>Общая цена</b>: {price}\n"
    for block in blocks:
        name = block.get("name", None)
        price = block.get("price", None)
        amount = block.get("amount", None)
        options = block.get("options", None)
        if len(options):
            string += (
                f'<b>Блок "{name}"</b>:\n'
                f"  • <i>Цена</i> - {price}\n"
                f"  • <i>Кол-во</i> - {amount}\n"
                "  • <b>Опции блока</b>:\n"
            )
            for option in options:
                option_name = option.get("name", None)
                option_value = option.get("value", None)
                string += f"     ◦ <i>{option_name}</i> - {option_value}\n"
        products_category = block.get("products_category", None)
        if len(products_category):
            string += "  • <b>Подходящие товары</b>:\n"
            for category_products in products_category:
                category = ProductType.objects.get(
                    id=category_products.get("category_id", None)
                ).name
                products = category_products.get("products", None)
                string += f"     ◦ <i>Категория товара (админка)</i> - {category}\n     ◦ <b>Товары</b>:\n"
                for product in products:
                    product_name = product.get("model", None)
                    product_category = product.get("category", None)
                    product_category_name = (
                        product_category.get("title", None)
                        if product_category
                        else "Отсутствует"
                    )
                    product_id = product.get("id", None)
                    product_price = product.get("price", None)
                    string += (
                        f"        ∙ <i>Модель</i> - {product_name}\n"
                        f"        ∙ <i>Категория</i> - {product_category_name}\n"
                        f"        ∙ <i>Цена</i> - {product_price}\n"
                        f"        --> <a href='{settings.DOMAIN}/products/{product_id}'>Ссылка на товар</a>\n"
                        "         ________________\n"
                    )
    return string


@shared_task
def send_calc_application(data: dict) -> bool:
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    chats = TelegramChat.objects.filter(send_application=True)
    string = (
        "<b><i>Получена новая заявка по калькулятору.</i></b>\n\n"
        f"<i>Имя</i> - {data.get('name')}\n"
        f"<i>Email</i> - {data.get('email')}\n"
        f"<i>Телефон</i> - {data.get('phone')}\n"
    )
    comment = data.get("comment", None)
    if comment:
        string += f"<b>Комментарий</b>:\n{comment}\n"
    string += "\n" + form_message_calculator_app(data.get("calculator_data"))
    for chat in chats:
        params = {
            "chat_id": chat.chat_id,
            "text": string,
            "parse_mode": "HTML",
            "link_preview_options": {"is_disabled": True},
        }
        requests.post(url, json=params)
    return True


@shared_task
def send_solution_application(data: dict) -> bool:
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    chats = TelegramChat.objects.filter(send_application=True)
    string = (
        "<b><i>Получена новая заявка по готовому решению.</i></b>\n\n"
        f"<i>Имя</i> - {data.get('name')}\n"
        f"<i>Email</i> - {data.get('email')}\n"
        f"<i>Телефон</i> - {data.get('phone')}\n"
    )
    comment = data.get("comment", None)
    if comment:
        string += f"<b>Комментарий</b>:\n{comment}\n"
    solution = ReadySolution.objects.get(id=data.get("solution"))
    string += "\n" + (
        f"<b>Готовое решение</b>:\n"
        f"  • <i>Название</i> - {solution.title}\n"
        f"  • <i>Цена</i> - {solution.price}\n"
        f"  --> <a href='{settings.DOMAIN}/sets/{solution.id}'>Ссылка на готовое решение</a>\n"
    )
    for chat in chats:
        params = {
            "chat_id": chat.chat_id,
            "text": string,
            "parse_mode": "HTML",
            "link_preview_options": {"is_disabled": True},
        }
        requests.post(url, json=params)
    return True


@shared_task
def send_file_application(data: dict) -> bool:
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}"
    chats = TelegramChat.objects.filter(send_application=True)
    string = (
        "<b><i>Получена новая заявка.</i></b>\n\n"
        f"<i>Имя</i> - {data.get('name')}\n"
        f"<i>Email</i> - {data.get('email')}\n"
        f"<i>Телефон</i> - {data.get('phone')}\n"
    )
    comment = data.get("comment", None)
    if comment:
        string += f"<b>Комментарий</b>:\n{comment}\n"
    file_path: str = data.get("file", None)
    file_id = None
    for chat in chats:
        params = {
            "chat_id": chat.chat_id,
            "parse_mode": "HTML",
        }
        if file_path:
            params["caption"] = string
            if file_id:
                params["document"] = file_id
                response = requests.post(f"{url}/sendDocument", data=params)
            else:
                full_file_path = os.path.join(settings.BASE_DIR, file_path)
                with open(full_file_path, "rb") as document:
                    response = requests.post(
                        f"{url}/sendDocument", data=params, files={"document": document}
                    )
                data = response.json()
                if data["ok"]:
                    file_id = data["result"]["document"]["file_id"]
        else:
            params["text"] = string
            params["link_preview_options"] = {"is_disabled": True}
            response = requests.post(f"{url}/sendMessage", json=params)
    return True
