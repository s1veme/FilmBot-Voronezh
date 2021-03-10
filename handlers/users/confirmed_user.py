from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsUserConfirmed

from keyboards.inline.choice_films import generate_all_films, create_choice_timetable, keyboard_menu, create_choice_cinema

from loader import dp, bot

from utils.json_actions.get_films import get_films_json

from ast import literal_eval
from datetime import datetime


def get_name_film(film_id, films):
    for film in films:
        if films[film]['_id'] == film_id:
            return film


@dp.message_handler(IsUserConfirmed(), CommandStart())
async def bot_start(message: Message, mode='text'):

    films = get_films_json()
    choice_films = generate_all_films(films)

    text = '*Все фильмы в Воронеже:*\n\n'

    for film in films:
        text += f"{film} - ( Рейтинг: *{films[film]['rating'][:3]}* )\n"

    if mode == 'text':
        return await message.answer(text, reply_markup=choice_films, parse_mode="MARKDOWN")
    elif mode == 'edit':
        return await bot.edit_message_text(text=text, reply_markup=choice_films, parse_mode="MARKDOWN", message_id=message.message_id, chat_id=message.chat.id)
    elif mode == 'posters':
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return await message.answer(text, reply_markup=choice_films, parse_mode="MARKDOWN")


@dp.callback_query_handler(IsUserConfirmed(), text_contains="film")
async def choice_timetable(call: CallbackQuery):
    films = get_films_json()

    film_id = literal_eval(call.data[5:])

    name_film = get_name_film(film_id, films)

    markup = create_choice_timetable(film_id, films[name_film]['trailer'])

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    img = open(f'posters/{film_id}.png', 'rb')
    await bot.send_photo(call.from_user.id, img,
                         caption=f"{name_film}\n\n{films[name_film]['description']}", reply_markup=markup)
    img.close()


@dp.callback_query_handler(IsUserConfirmed(), text_contains="all")
async def get_timetable_all(call: CallbackQuery):
    films = get_films_json()

    film_id = literal_eval(call.data[4:])
    text = ''
    content = ''

    now = datetime.now().strftime('%H:%M')

    name_film = get_name_film(film_id, films)

    for film in films[name_film]['timetable']:
        for time in films[name_film]["timetable"][film]["time"]:
            if time[0] >= now:
                content += f" {time[0]} (<i>{time[1]}</i>);"
            else:
                content += f" <s>{time[0]} (<i>{time[1]}</i>)</s>;"

        text += f"{film} - {content}\n\n"

        content = ""
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await call.message.answer(text=text, reply_markup=keyboard_menu, parse_mode='html')


@dp.callback_query_handler(IsUserConfirmed(), text_contains="cinema")
async def choice_cinema(call: CallbackQuery):
    films = get_films_json()

    film_id = literal_eval(call.data[7:])

    name_film = get_name_film(film_id, films)

    markup = create_choice_cinema(
        name_film=name_film, film_id=film_id, films=films)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(text='Список Кинотеатров 🎥', reply_markup=markup)


@dp.callback_query_handler(IsUserConfirmed(), text_contains="mov")
async def get_timetable_film(call: CallbackQuery):
    films = get_films_json()

    now = datetime.now().strftime('%H:%M')

    film_info = call.data[4:].split(':')

    film_id = int(film_info[0])
    cinema_id = int(film_info[1])

    name_film = get_name_film(film_id, films)

    for cinema in films[name_film]["timetable"]:
        if cinema_id == films[name_film]["timetable"][cinema]['_id']:
            cinema_title = cinema
            break

    timetable = f'Расписание в {cinema_title}:\n'

    for time in films[name_film]["timetable"][cinema_title]["time"]:
        if time[0] >= now:
            timetable += f'{time[0]} (<i>{time[1]}</i>)\n'
        else:
            timetable += f'<s>{time[0]} (<i>{time[1]}</i>)</s>\n'

    await call.bot.edit_message_text(text=timetable, reply_markup=keyboard_menu, parse_mode="html", message_id=call.message.message_id, chat_id=call.message.chat.id)


@dp.callback_query_handler(IsUserConfirmed(), text_contains="menu")
async def get_menu(call: CallbackQuery):
    mode = call.data[5:]

    if mode == 'posters':
        await bot_start(call.message, mode='posters')
    else:
        await bot_start(call.message, mode='edit')
