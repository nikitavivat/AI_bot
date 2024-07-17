import config
import database

start_msg = ('Привет! Данный бот предназначен для упрощенног овзаимодействия с языковыми моделями.\n\n'
             'В данном боте ты можешь использовать:\n'
             '- ChatGPT 3.5 (бесплатно, с ограничением количества запросов в сутки)\n'
             '- ChatGPT 4o (платно, с 3 бесплатными запросами за все время)\n'
             '- Gemini Flash (бесплатно, с ограничением количества запросов в сутки)\n'
             '- Gemini Pro (платно, с 3 бесплатными запросами за все время)\n\n'
             'Для просмотра всех команд: /help')

help_msg = ('/start: Описание возможностей бота, доступные модели и инструкция по использованию.\n\n'
            '/account: Информация о доступных подписках и оставшихся генерациях каждой модели.)\n\n'
            '/premium: Информация о премиум-подписках, стоимость и кнопки для покупки премиум-подписок (ChatGPT 4o и Gemini Pro).\n\n'
            '/settings: Выбор языковой модели или генерации изображения.\n\n'
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

🟢 Gemini Flash
Скорость: 
Интеллект: 



🟢 Gemini Pro

''')

DALL_E_msg = ('В текущем режиме будут генерироваться изображения, а не текст🏞️\n'
                                    '\nМодель генерации: DALL-E 3')

chanel_msg = ('Для взаимодействия с ботом нужно подписаться на канал:\n'
                                        f'{config.tg_chanel}')

db = database.Database()

def account_msg(user_id):
    text = f"""
👨‍💻 Пользователь: {user_id}

📎 Оставшиеся отклики:
- GPT 3.5: {int(db.get_ChatGPT_35_per_day(user_id)) + int(db.get_GPT_35(user_id))}
- GPT 4o: {int(db.get_ChatGPT_4o_per_day(user_id)) + int(db.get_GPT_4o(user_id))}
- Gemini Flash: {int(db.get_Gemini_Flash_per_day(user_id)) + int(db.get_Gemini_Flash(user_id))}
- Gemini Pro: {int(db.get_Gemini_Pro_per_day(user_id)) + int(db.get_Gemini_Pro(user_id))}
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