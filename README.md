## README.md

Описание проекта:

Этот проект представляет собой телеграм-бота, который предоставляет доступ к различным языковым моделям, таким как ChatGPT, ChatGPT Flash и ChatGPT Pro, а также генерации изображений с помощью DALL-E 3.

__Структура проекта:__

• config.py: Содержит конфигурационные данные, такие как токены API, ID каналов, цены на подписки и другие константы.
• database.py: Обеспечивает взаимодействие с базой данных для хранения информации о пользователях, их подписках, балансе и других данных.
• messages.py: Содержит тексты сообщений, отправляемых ботом пользователям.
• main.py: Основной файл, запускающий бота.

__Инструкции по запуску:__

1. Создайте бота в Telegram:
  - Найдите бота @BotFather в Telegram.
  - Используйте команду /newbot для создания нового бота.
  - Запишите токен бота, который будет использован в config.py.
2. Создайте канал в Telegram:
  - Создайте канал в Telegram.
  - Запишите ID канала (в формате -100XXXXXXXXX) в config.py.
3. Получите API ключи:
  - Получите API ключи для ChatGPT (3.5 и 4.0), ChatGPT Flash и ChatGPT Pro от OpenAI.
  - Получите API ключ для DALL-E 3 от OpenAI.
  - Запишите эти ключи в config.py.
4. Установите зависимости:
  - Используйте pip install -r requirements.txt для установки необходимых библиотек.
5. Запустите бота:
  - Используйте python main.py для запуска бота.

__Конфигурационный файл (config.py):__
```
tg_chanel = "your_chanel_link"
chanel_id = "your_chanel_id"

BOT_TOKEN = "your_bot_token"

GEMINI_API_KEY = "your_gemini_api_key"
GPT_API_KEY = "your_gpt_api_key"

ChatGPT_35_free_per_day = 100
ChatGPT_4o_free_per_day = 3
ChatGPT_Flash_free_per_day = 100
ChatGPT_Pro_free_per_day = 3
DALLE3_free_per_day = 3

PREMIUM_PRICE = 290

PRICE_PER_ONE_GPT_35 = 5
PRICE_PER_ONE_GPT_4o = 9.9
PRICE_PER_ONE_GEMINI_FLASH_PER_ONE = 30
PRICE_PER_ONE_GEMINI_PER_ONE = 9.9
PRIME_STATUS_PER_DAY = 1000
DALLE3_PER_ONE = 9.9

owners = []

"""
Обозначения для тарифов:
gpt35 - GPT 3.5
gpt4o - GPT 4.o
gf - ChatGPT Flash
gp - ChatGPT Pro
"""
#tariff_plans = ['tariff_premium', 'tariff_gpt35_10', 'tariff_gpt4o_10', 'tariff_gf_10', 'tariff_gp_11']
#name_of_tariff_plans = ['Премиум тариф', 'GPT 3.5 - 10 запросов', 'GPT 4o - 10 запросов',
#                        'ChatGPT Flash - 10 запросов', 'ChatGPT PRO - 11 запросов']
tariff_plans = ['tariff_gpt4o_10', 'tariff_gp_10', 'tariff_dalle3_10']
name_of_tariff_plans = ['GPT 4o 10 запросов - 99 руб', 'ChatGPT Pro 10 запросов - 99 руб', 'DALL-E 3 10 запросов - 99 руб']
```
Сообщения (messages.py):
```
import config
import database

start_msg = ('Привет! Данный бот предназначен для упрощенног овзаимодействия с языковыми моделями.nn'
             'В данном боте ты можешь использовать:n'
             '- ChatGPT 3.5 (бесплатно, с ограничением количества запросов в сутки)n'
             '- ChatGPT 4o (платно, с 3 бесплатными запросами за все время)n'
             '- ChatGPT Flash (бесплатно, с ограничением количества запросов в сутки)n'
             '- ChatGPT Pro (платно, с 3 бесплатными запросами за все время)nn'
             'Для просмотра всех команд: /help')

help_msg = ('/start: Описание возможностей бота, доступные модели и инструкция по использованию.nn'
            '/account: Информация о доступных подписках и оставшихся генерациях каждой модели.)nn'
            '/premium: Информация о премиум-подписках, стоимость и кнопки для покупки премиум-подписок (ChatGPT 4o и ChatGPT Pro).nn'
            '/settings: Выбор языковой модели или генерации изображения.nn'
            '/image: Генерация изображения (использует DALL-E 3).')

settings_message = (f'''
Давай выберем модель ИИ:

🟢 GPT_3.5_Turbo - оригинальный движок ChatGPT
Скорость: 5/5
Интеллект: 3/5
Доступно бесплатно: ✅

🟢 GPT-4o
Скорость: 4/5
Интеллект: 5/5
Доступно бесплатно: 3 запроса в день, далее платно✅

🟢 ChatGPT Flash
Скорость: 
Интеллект: 



🟢 ChatGPT Pro

''')

DALL_E_msg = ('В текущем режиме будут генерироваться изображения, а не текст🏞️n'
                                    'nМодель генерации: DALL-E 3')

chanel_msg = ('Для взаимодействия с ботом нужно подписаться на канал:n'
                                        f'{config.tg_chanel}')

db = database.Database()

def account_msg(user_id):
    text = f"""
👨‍💻 Пользователь: {user_id}

📎 Оставшиеся отклики:
- GPT 3.5: {int(db.get_ChatGPT_35_per_day(user_id)) + int(db.get_GPT_35(user_id))}
- GPT 4o: {int(db.get_ChatGPT_4o_per_day(user_id)) + int(db.get_GPT_4o(user_id))}
- ChatGPT Flash: {int(db.get_ChatGPT_Flash_per_day(user_id)) + int(db.get_ChatGPT_Flash(user_id))}
- ChatGPT Pro: {int(db.get_ChatGPT_Pro_per_day(user_id)) + int(db.get_ChatGPT_Pro(user_id))}
- DALL-E 3: {int(db.get_DALLE3_per_day(user_id)) + int(db.get_DALLE3(user_id))}
Ваша подписка: {db.get_premium_status(user_id)}
Ваш баланс: {db.get_user_balance(user_id)}

🤖 Текущая модель генерации: {db.get_current_model(user_id)}

Посмотреть все команды: /help
    """
    return text

def premium_msg(user_id):
    prime_msg = f"""
🍓Премиум даст вам 50 запрсоов ко всем моделям!
Цена: 290 руб.

💥 Дополнительно запросы можно купить по цене 99 руб. за 10 запросов, если запросы закончились.
• запросы суммируются, поэтому никогда не пропадут
"""
    return prime_msg
```
__Редактирование сообщений (messages.py):__

В файле messages.py вы можете редактировать текст сообщений, отправляемых ботом пользователям. 

Запуск бота (main.py):

Файл main.py содержит основной код, который запускает бота. 
Важно: убедитесь, что вы заполнили все конфигурационные данные в config.py перед запуском бота. 

Дополнительные замечания:

• База данных: Для хранения информации о пользователях рекомендуется использовать базу данных.
• Логирование: Рекомендуется использовать логирование для отслеживания ошибок и событий.
• Тестирование: Важно проводить тестирование бота для обеспечения его правильной работы.

Дополнительные возможности:

• Добавить возможность оплаты подписок через платежные системы.
• Добавить возможность выбора языка для генерации текста.
• Добавить возможность настройки дополнительных параметров для языковых моделей.

Полезные ссылки:

• Документация Telegram Bot API
• Документация OpenAI
• Библиотека python-telegram-bot

Важно:

• Безопасность: Защитите свои API ключи, не храните их в открытом доступе.
• Правовая ответственность: Убедитесь, что использование бота не нарушает законодательство.
