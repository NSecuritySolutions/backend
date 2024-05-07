import time
import os

from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from telegram import Bot
from telegram.utils.request import Request
from application.models import Application

load_dotenv()

class Command(BaseCommand):
    help = "Телеграм-бот"

    def handle(self, *args, **options):
        # Инициализация объекта Request для настройки таймаутов при запросах
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        
        # Инициализация объекта Bot с использованием токена из настроек Django
        bot = Bot(
            request=request,
            token=os.getenv('TELEGRAM_TOKEN'),
        )
        
        # Вывод информации о боте
        print(bot.get_me())

        while True:
            try:
                # Получение данных напрямую из базы данных Django
                queryset = Application.objects.filter(processed=False)  
                # Предполагается, что у вас есть модель с полями, подобными данным вашего запроса

                for data in queryset:
                    # Формирование сообщения из полученных данных
                    message = (
                        f"Новая заявка получена!\n"
                        f"Имя: {data.name}\n"
                        f"Комментарий: {data.description}\n"
                        f"Почта: {data.email}\n"
                        f"Номер телефона: {data.number}\n"
                        f"Повод заявки: Просто Заявка"
                    )

                    # Отправка отформатированного сообщения конкретному пользователю
                    user_id_to_notify = 1684336348
                    bot.send_message(chat_id=user_id_to_notify, text=message)

                    # Помечаем данные как обработанные
                    data.processed = True
                    data.save()

            except Exception as e:
                print(f"Произошла ошибка: {e}")

            # Пауза перед следующим запросом
            time.sleep(5)  # Например, делаем запрос каждые 5 секунд