import asyncio
import logging
from random import randint

import importlib

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import config
import database
import messages
import models
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = database.Database()

last_admin_move = {}


def create_keyboard_models(user_id):
    """
    Создает клавиатуру для выбора моделей на основе текущей модели пользователя.
    """

    periods_kb = InlineKeyboardBuilder()

    if db.get_current_model(user_id) == "GPT 3.5":
        periods_kb.add(types.InlineKeyboardButton(
            text=f"✅GPT 3.5",
            callback_data=f"models_gpt3.5")
        )
    else:
        periods_kb.add(types.InlineKeyboardButton(
            text=f"GPT 3.5",
            callback_data=f"models_gpt3.5")
        )
    if db.get_current_model(user_id) == "GPT 4o":
        periods_kb.add(types.InlineKeyboardButton(
            text=f"✅GPT 4o",
            callback_data=f"models_gpt4o")
        )
    else:
        periods_kb.add(types.InlineKeyboardButton(
            text=f"GPT 4o",
            callback_data=f"models_gpt4o")
        )
    if db.get_current_model(user_id) == "Gemini Flash":
        periods_kb.add(types.InlineKeyboardButton(
            text=f"✅Gemini Flash",
            callback_data=f"models_geminiflash")
        )
    else:
        periods_kb.add(types.InlineKeyboardButton(
            text=f"Gemini Flash",
            callback_data=f"models_geminiflash")
        )
    if db.get_current_model(user_id) == "Gemini PRO":
        periods_kb.add(types.InlineKeyboardButton(
            text=f"✅Gemini PRO",
            callback_data=f"models_geminipro")
        )
    else:
        periods_kb.add(types.InlineKeyboardButton(
            text=f"Gemini PRO",
            callback_data=f"models_geminipro")
        )
    if db.get_current_model(user_id) == "DALL-E 3":
        periods_kb.add(types.InlineKeyboardButton(
            text=f"✅DALL-E 3",
            callback_data=f"models_geminipro")
        )
    else:
        periods_kb.add(types.InlineKeyboardButton(
            text=f"DALL-E 3",
            callback_data=f"models_dalle3")
        )

    periods_kb.adjust(2)

    return periods_kb.as_markup()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Обрабатывает команду /start, проверяет подписку пользователя и отправляет приветственное сообщение.
    """

    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, messages.chanel_msg)
        return False
    if not user_id in db.get_all_ids():
        db.insert_user(user_id, message.from_user.username)
    await bot.send_message(user_id, messages.start_msg)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Обрабатывает команду /help, проверяет подписку пользователя и отправляет сообщение с помощью.
    """

    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, )
        return False
    await bot.send_message(user_id, messages.help_msg)


@dp.message(Command("account"))
async def cmd_account(message: types.Message):
    """
    Обрабатывает команду /account, проверяет подписку пользователя и отправляет информацию об аккаунте.
    """

    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, messages.chanel_msg)
        return False

    await bot.send_message(user_id, messages.account_msg(user_id))
    await bot.delete_message(user_id, message.message_id)


@dp.message(Command("premium"))
async def cmd_premium(message: types.Message):
    """
    Обрабатывает команду /premium, проверяет подписку пользователя и отправляет информацию о премиум тарифах.
    """

    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, messages.chanel_msg)
        return False
    periods_kb = InlineKeyboardBuilder()
    for i in range(len(config.tariff_plans)):
        periods_kb.add(types.InlineKeyboardButton(
            text=config.name_of_tariff_plans[i],
            callback_data=config.tariff_plans[i])
        )
    periods_kb.adjust(1)
    await bot.send_message(user_id, messages.premium_msg(user_id), reply_markup=periods_kb.as_markup())
    await bot.delete_message(user_id, message.message_id)


@dp.callback_query(F.data.startswith("tariff_"))
async def cmd_tariff(callback: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку с тарифом, отправляет информацию об оплате.
    """

    user_id = callback.from_user.id
    t = callback.data.split("_")[1]
    periods_kb = InlineKeyboardBuilder()
    if t == 'premium':
        periods_kb.add(types.InlineKeyboardButton(
            text=f"100 руб",
            callback_data=f"payed_premium")
        )
        await bot.edit_message_text(text='Оплатите тариф', chat_id=user_id, message_id=callback.message.message_id,
                                    reply_markup=periods_kb.as_markup())
    else:
        count_of_voice = int(callback.data.split("_")[2])
        if t == 'gpt35':
            price = count_of_voice * float(config.PRICE_PER_ONE_GPT_35)
        elif t == 'gpt4o':
            price = count_of_voice * float(config.PRICE_PER_ONE_GPT_4o)
        elif t == 'gf':
            price = count_of_voice * float(config.PRICE_PER_ONE_GEMINI_PER_ONE)
        elif t == 'gp':
            price = count_of_voice * float(config.PRICE_PER_ONE_GEMINI_PER_ONE)
        elif t == 'dalle3':
            price = count_of_voice * float(config.DALLE3_PER_ONE)
        else:
            return False
        periods_kb.add(types.InlineKeyboardButton(
            text=f"{price} руб",
            callback_data=f"payed_{t}_{count_of_voice}")
        )
        await bot.edit_message_text(text=f'Оплатите запросы на сумму {price} руб.', chat_id=user_id,
                                    message_id=callback.message.message_id,
                                    reply_markup=periods_kb.as_markup())


@dp.callback_query(F.data.startswith("payed_"))
async def cmd_tariff(callback: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку оплаты тарифа, обновляет статус в базе данных.
    """

    user_id = callback.from_user.id
    t = callback.data.split("_")[1]
    if t == 'premium':
        db.update_premium_status(user_id, 'YES')
        await bot.send_message(user_id, 'Премиум тариф оплачен и успешно применен')
    else:
        count_of_voice = int(callback.data.split("_")[2])
        if t == 'gpt35':
            restriction = int(db.get_GPT_35(user_id))
            db.update_GPT_35(user_id, restriction + count_of_voice)
        elif t == 'gpt4o':
            restriction = int(db.get_GPT_4o(user_id))
            db.update_GPT_4o(user_id, restriction + count_of_voice)
        elif t == 'gf':
            restriction = int(db.get_Gemini_Flash(user_id))
            db.update_Gemini_Flash(user_id, restriction + count_of_voice)
        elif t == 'gp':
            restriction = int(db.get_Gemini_Pro(user_id))
            db.update_Gemini_Pro(user_id, restriction + count_of_voice)
        elif t == 'dalle3':
            restriction = int(db.get_DALLE3(user_id))
            db.update_dalle3(user_id, restriction + count_of_voice)
        else:
            return False
        await bot.send_message(user_id, 'Отклики успешно оплачены')


@dp.message(Command("settings"))
async def cmd_settings(message: types.Message):
    """
    Обрабатывает команду /settings, проверяет подписку пользователя и отправляет клавиатуру для выбора модели.
    """

    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, messages.chanel_msg)
        return False

    periods_kb = create_keyboard_models(user_id)

    await bot.send_message(user_id, messages.settings_message, reply_markup=periods_kb)
    await bot.delete_message(user_id, message.message_id)


@dp.callback_query(F.data.startswith('models_'))
async def get_choose_models(callback: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку выбора модели, обновляет текущую модель в базе данных.
    """

    user_id = callback.from_user.id
    data = callback.data.split('_')[1]
    print(data)
    if data == 'gpt3.5':
        data = 'GPT 3.5'
    elif data == 'gpt4o':
        data = 'GPT 4o'
    elif data == 'geminiflash':
        data = 'Gemini Flash'
    elif data == 'geminipro':
        data = 'Gemini PRO'
    elif data == 'models_dalle3':
        data = 'DALL-E 3'
    db.update_current_model(user_id, data)
    kb = create_keyboard_models(user_id)
    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=kb)


@dp.message(Command("image"))
async def cmd_image(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, messages.chanel_msg)
        return False
    db.update_current_model(user_id, 'DALL-E 3')
    await bot.send_message(user_id, messages.DALL_E_msg)
    await bot.delete_message(user_id, message.message_id)


class Admin(StatesGroup):
    give_premium = State()
    delete_premium = State()
    update_balance = State()
    count_of_money = State()


@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status == 'owner' or user_id in config.owners:
        if_user_subscribed = True
    else:
        if_user_subscribed = False
    if not if_user_subscribed:
        return False
    kb = [
        [
            types.KeyboardButton(text="Выдать подписку"),
            types.KeyboardButton(text="Забрать подписку")
        ],
        [
            types.KeyboardButton(text="Обновить баланс")
        ],
    ]

    keyboard_admin = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await bot.send_message(user_id, "Выберите действие", reply_markup=keyboard_admin)


@dp.message(F.text == "Выдать подписку")
async def send_premium(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'Введите username пользователя, для выдачи подписки, пример:\n@example')
    await state.set_state(Admin.give_premium)


@dp.message(F.text == "Забрать подписку")
async def send_premium(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'Введите username пользователя, для удаления подписки, пример:\n@example')
    await state.set_state(Admin.delete_premium)


@dp.message(F.text == "Обновить баланс")
async def send_premium(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'Введите username пользователя, для обновления баланса, пример:\n@example')
    await state.set_state(Admin.update_balance)


@dp.message(Admin.give_premium)
async def premium_give(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text
    db.update_prime_status_by_username(name, "YES")
    await bot.send_message(user_id, 'Премиум статус был выдан')
    await state.clear()


@dp.message(Admin.delete_premium)
async def premium_del(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text
    db.update_prime_status_by_username(name, "NO")
    await bot.send_message(user_id, 'Премиум статус был выдан')
    await state.clear()


@dp.message(Admin.update_balance)
async def bal_us_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text
    await state.update_data(username=name.replace('@', ''))
    await bot.send_message(user_id, 'Введите сумму которую хотите присвоить пользователю')
    await state.set_state(Admin.count_of_money)


@dp.message(Admin.count_of_money)
async def bal_us_count(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        count = int(message.text)
    except:
        await state.clear()
        await bot.send_message(user_id, 'Вы ввели не число, начните операцию заново')
        return False
    user_data = await state.get_data()
    db.update_balance_by_username(user_data['username'], count)
    await bot.send_message(user_id, 'Баланс пользователя был обновлен')
    await state.clear()


@dp.message(F.text)
async def generate(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await bot.get_chat_member(config.chanel_id, user_id)
    if is_subscribed.status != 'left':
        if_user_subscribed = True
    else:
        if_user_subscribed = False

    if not if_user_subscribed:
        await bot.send_message(user_id, messages.chanel_msg)
        return False

    current_model = db.get_current_model(user_id)
    if db.get_premium_status(user_id) == 'NO':
        if current_model == 'GPT 3.5':
            restriction = db.get_ChatGPT_35_per_day(user_id)
            if int(restriction) > 0:
                db.update_ChatGPT_35_per_day(user_id, int(restriction) - 1)
            else:
                payed_restriction = db.get_GPT_35(user_id)
                if not int(payed_restriction) > 0:
                    await bot.send_message(user_id, 'Вы превысили лимит на использование GPT 3.5')
                    return False
                else:
                    db.update_GPT_35(user_id, payed_restriction - 1)
        elif current_model == 'GPT 4o':
            restriction = db.get_ChatGPT_4o_per_day(user_id)
            if int(restriction) > 0:
                db.update_ChatGPT_4o_per_day(user_id, int(restriction) - 1)
            else:
                payed_restriction = db.get_GPT_4o(user_id)
                if not int(payed_restriction) > 0:
                    await bot.send_message(user_id, 'Вы превысили лимит на использование GPT 4o')
                    return False
                else:
                    db.update_GPT_4o(user_id, payed_restriction - 1)
        elif current_model == 'Gemini Flash':
            restriction = db.get_Gemini_Flash_per_day(user_id)
            if int(restriction) > 0:
                db.update_Gemini_Flash_per_day(user_id, int(restriction) - 1)
            else:
                payed_restriction = db.get_Gemini_Flash(user_id)
                if not int(payed_restriction) > 0:
                    await bot.send_message(user_id, 'Вы превысили лимит на использование GPT Gemini Flash')
                    return False
                else:
                    db.update_Gemini_Flash(user_id, payed_restriction - 1)
        elif current_model == 'Gemini PRO':
            restriction = db.get_Gemini_Pro_per_day(user_id)
            if int(restriction) > 0:
                db.update_Gemini_Pro_per_day(user_id, int(restriction) - 1)
                print(1)
            else:
                payed_restriction = db.get_Gemini_Pro(user_id)
                if not int(payed_restriction) > 0:
                    await bot.send_message(user_id, 'Вы превысили лимит на использование GPT Gemini PRO')
                    return False
                else:
                    db.update_Gemini_Pro(user_id, payed_restriction - 1)
        else:
            restriction = db.get_DALLE3_per_day(user_id)
            if int(restriction) > 0:
                db.update_dalle3_per_day(user_id, int(restriction) - 1)
            else:
                if not int(db.get_DALLE3(user_id)) > 0:
                    await bot.send_message(user_id, 'Вы превысили лимит на использование DALL-E 3')
                    return False
                else:
                    db.update_dalle3(user_id, int(db.get_DALLE3(user_id)) - 1)
    else:
        x = int(db.get_count_of_all_requests(user_id))
        if int(config.PRIME_STATUS_PER_DAY) > x:
            db.update_count_of_all_requests(user_id, x + 1)
        else:
            await bot.send_message(user_id, "Ваш лимит в тарифе премиум завершился")

    await bot.send_chat_action(message.chat.id, 'typing')
    await models.generate(current_model, str(message.text), bot, user_id)


async def new_day():
    users_id = db.get_all_ids()
    for user_id in users_id:
        db.update_ChatGPT_35_per_day(user_id, config.ChatGPT_35_free_per_day)
        db.update_ChatGPT_4o_per_day(user_id, config.ChatGPT_4o_free_per_day)
        db.update_Gemini_Flash_per_day(user_id, config.Gemini_Flash_free_per_day)
        db.update_Gemini_Pro_per_day(user_id, config.Gemini_Pro_free_per_day)
    await asyncio.sleep(86400)


async def start_polling():
    await dp.start_polling(bot)


async def main():
    """ Запуск бота """
    await asyncio.gather(
        new_day(),
        start_polling()
    )


if __name__ == "__main__":
    asyncio.run(main())
