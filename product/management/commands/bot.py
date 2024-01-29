from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.utils.request import Request
import requests
from application.models import Application

class Command(BaseCommand):
    help = "Телеграм-бот"

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        url = 'http://127.0.0.1:8000/create-application/'

        # Отправим POST-запрос на указанный URL с числовым значением для 'number'
        response = requests.post(url, data={'name': 'John', 'description': 'Some comment', 'email': 'john@example.com', 'number': 123456789})

        # Выведем на экран данные, отправленные и полученные
        print(f"Отправленные данные: {'name': 'John', 'description': 'Some comment', 'email': 'john@example.com', 'number': 123456789}")
        print(f"Полученные данные: {response.text}")

        # Проверим статус ответа
        if response.status_code == 200:
            # Если запрос успешен, выведите сообщение
            print("POST запрос успешно отправлен")
            
            # Создайте объект Application из полученных данных
            application_data = response.json()  # Предполагается, что сервер возвращает данные в формате JSON
            application = Application.objects.create(
                name=application_data.get('name', ''),
                description=application_data.get('description', ''),
                email=application_data.get('email', ''),
                number=application_data.get('number', '')
            )

            # Если user_id_to_notify совпадает, отправьте сообщение через бота
            user_id_to_notify = 1684336348
            if user_id_to_notify == user_id_to_notify:
                message = (
                    f"Новая заявка получена!\n"
                    f"Имя: {application.name}\n"
                    f"Комментарий: {application.description}\n"
                    f"Почта: {application.email}\n"
                    f"Номер телефона: {application.number}"
                )

                bot.send_message(chat_id=user_id_to_notify, text=message)

        else:
            # Если запрос неудачен, выведите ошибку
            print(f"Ошибка при отправке POST запроса: {response.status_code}")