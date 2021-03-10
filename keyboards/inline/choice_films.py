from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import choice_timetable_callback, all_timetable_callback, choice_cinema, get_timetable_cinema

menu = InlineKeyboardButton(text="Меню", callback_data=f"menu")

keyboard_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        menu
    ]
])


def generate_all_films(films):
    choice_films = InlineKeyboardMarkup(row_width=2)
    for film in films:
        btn = InlineKeyboardButton(
            text=film, callback_data=choice_timetable_callback.new(film_id=films[film]['_id']))

        choice_films.insert(btn)

    return choice_films


def create_choice_timetable(film_id, tailer_url):
    menu = InlineKeyboardButton(text="Меню", callback_data=f"menu_posters")
    choice_timetable = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Вывести всё расписание",
                                 callback_data=all_timetable_callback.new(film_id=film_id)),
            InlineKeyboardButton(text="Выбрать кинотеатр",
                                 callback_data=choice_cinema.new(film_id=film_id))
        ],
        [
            InlineKeyboardButton(text="Трейлер", url=tailer_url)
        ],
        [
            menu
        ]
    ])

    return choice_timetable


def create_choice_cinema(film_id, name_film, films):
    markup = InlineKeyboardMarkup(row_width=2)

    for cinema in films[name_film]['timetable']:
        btn = InlineKeyboardButton(text=cinema, callback_data=get_timetable_cinema.new(
            film_id=film_id, cinema_id=films[name_film]['timetable'][cinema]['_id']))
        markup.insert(btn)
    markup.add(menu)

    return markup
