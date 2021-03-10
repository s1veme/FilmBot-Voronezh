import json


def get_films_json():
    with open("info.txt", 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data


def write_json(films: str):
    with open("info.txt", 'w', encoding='utf-8') as file:
        json.dump(films, file, ensure_ascii=False)
