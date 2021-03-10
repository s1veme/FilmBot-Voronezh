from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import sqlite 

from loader import bot

class IsNewUser(BoundFilter):
    """
        Регистрация нового пользователя
    """
    
    async def check(self, message: types.Message):
        return sqlite.check_new_user(message.from_user.id)

class IsUserConfirmed(BoundFilter):

    """
        Проверка, есть ли пользователь в базе данных
    """
    
    async def check(self, message: types.Message):
        return sqlite.check_user(message.from_user.id)