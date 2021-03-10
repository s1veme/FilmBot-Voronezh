from aiogram import Dispatcher
import logging

from .user_filters import IsNewUser, IsUserConfirmed
from .admin_filters import IsAdmin


def setup(dp: Dispatcher):
    logging.info("Подключение filters...")
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]

    dp.filters_factory.bind(IsNewUser)
    dp.filters_factory.bind(IsUserConfirmed)
    dp.filters_factory.bind(IsAdmin)