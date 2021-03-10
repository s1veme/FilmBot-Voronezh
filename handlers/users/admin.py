from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from filters import IsAdmin

from loader import dp, bot

from utils.db_api import sqlite


@dp.message_handler(IsAdmin(), Command(commands=['add_user'], prefixes='/'))
async def add_user(message: Message):
    argument = message.get_args()

    try:

        if sqlite.check_user(argument) == False:
            sqlite.confirm_user(argument)

            await message.reply(f"Пользователь с {argument} - успешно добавлен")

            await bot.send_message(chat_id=argument, text='Рады вас приветствовать в нашем боте!\n\n_Подписка успешно оформлена._\n\n*Для начала работы напишите /start*', parse_mode="MARKDOWN")

        else:
            await message.reply(f"Пользователь {argument} уже имеет подписку!")

    except Exception as e:
        await message.reply(f"Ошибка!", e)


@dp.message_handler(IsAdmin(), Command(commands=['all_clients'], prefixes='/'))
async def get_clients(message: Message):
    count_clients = sqlite.get_all_clients()
    count_users = sqlite.get_all_users()

    await message.reply(f'Купили: {count_clients}\nОбычных пользователей: {count_users}\n\nВсего: {count_clients + count_users}')
