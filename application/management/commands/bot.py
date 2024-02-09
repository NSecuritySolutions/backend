import requests
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.utils.request import Request

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
            token=settings.TOKEN,
        )
        
        # Вывод информации о боте
        print(bot.get_me())

        processed_ids = set()  # Множество для хранения обработанных идентификаторов

        while True:
            try:
                # URL для запроса данных у Django-сервера
                url = "http://localhost:8000/application/"

                # Выполнение GET-запроса к Django-серверу
                response = requests.get(url)

                if response.status_code == 200:
                    # Раскомментировать строку ниже для вывода содержимого ответа
                    # print(response.content)
                    data = response.json()

                    # Проверка, был ли обработан данный идентификатор
                    if data['id'] not in processed_ids:
                        processed_ids.add(data['id'])  # Добавление идентификатора в множество обработанных

                        # if data['occasion'] == 'ONE':
                        #     occasion = 'Просто заявка'
                        # elif data['occasion'] == 'TWO':
                        #     occasion = 'Калькулятор'
                        # else:
                        #     occasion = 'Not Found'

                        # Формирование сообщения из полученных данных
                        message = (
                            f"Новая заявка получена!\n"
                            f"Имя: {data['name']}\n"
                            f"Комментарий: {data['description']}\n"
                            f"Почта: {data['email']}\n"
                            f"Номер телефона: {data['number']}\n"
                            f"Повод заявки: Просто Заявка"
                        )

                        # Отправка отформатированного сообщения конкретному пользователю
                        user_id_to_notify = 1684336348
                        bot.send_message(chat_id=user_id_to_notify, text=message)

                else:
                    print(f"Ошибка: {response.status_code}")
            
                # # URL для запроса данных у Django-сервера
                # cal_url = "http://127.0.0.1:8000/api/v1/camera/"

                # # Выполнение GET-запроса к Django-серверу
                # cal_response = requests.get(cal_url)

                # if cal_response.status_code == 200:
                #     # Раскомментировать строку ниже для вывода содержимого ответа
                #     # print(response.content)
                #     data1 = cal_response.json()

                #     # Проверка, был ли обработан данный идентификатор
                #     if cal_response['id'] not in processed_ids:
                #         processed_ids.add(cal_response['id'])  # Добавление идентификатора в множество обработанных

                #         # if data['occasion'] == 'ONE':
                #         #     occasion = 'Просто заявка'
                #         # elif data['occasion'] == 'TWO':
                #         #     occasion = 'Калькулятор'
                #         # else:
                #         #     occasion = 'Not Found'

                #         # Формирование сообщения из полученных данных
                #         message = (
                #             f"Новая заявка получена!\n"
                #             f"Имя: {data['name']}\n"
                #             f"Комментарий: {data['description']}\n"
                #             f"Почта: {data['email']}\n"
                #             f"Номер телефона: {data['number']}\n"
                #             f"Характеристики:\n"
                #             f""
                #         )

                #         # Отправка отформатированного сообщения конкретному пользователю
                #         user_id_to_notify = 1684336348
                #         bot.send_message(chat_id=user_id_to_notify, text=message)

                # else:
                #     print(f"Ошибка: {response.status_code}")

            except Exception as e:
                print(f"Произошла ошибка: {e}")

            # Пауза перед следующим запросом
            time.sleep(5)  # Например, делаем запрос каждые 5 секунд
