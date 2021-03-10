from aiogram.utils.callback_data import CallbackData

choice_timetable_callback = CallbackData("film", "film_id")
all_timetable_callback = CallbackData("all", "film_id")
choice_cinema = CallbackData("cinema", "film_id")
get_timetable_cinema = CallbackData("mov", "film_id", "cinema_id")
