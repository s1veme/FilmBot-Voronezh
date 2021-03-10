from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command

from utils.db_api import sqlite

from filters import IsNewUser

from loader import dp, bot


@dp.message_handler(CommandStart())
async def send_start_confirmed(message: Message):

    sqlite.check_new_user(message.from_user.id)

    text = f'Оплатите подписку 💰\nСтоимость <b>99р</b>.\nПеревод осуществляется по номеру карты <b></b>\nС обязательным комментарием <b>{message.from_user.id}</b>\n\nОбязательно перед покупкой прочтите <a href="">пользовательское соглашение</a>\n\n<b>Подписка будет выдана в течение 15 минут</b>'

    return await message.answer(text, parse_mode="html")
