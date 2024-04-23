from flask import Flask, request, jsonify
import logging
import random


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

regions = {
    "Республика Адыгея": "Майкоп",
    "Республика Башкортостан": "Уфа",
    "Республика Бурятия": "Улан-Удэ",
    "Республика Алтай": "Горно-Алтайск",
    "Республика Дагестан": "Махачкала",
    "Республика Ингушетия": "Магас",
    "Республика Кабардино-Балкария": "Нальчик",
    "Республика Калмыкия": "Элиста",
    "Республика Карачаево-Черкесия": "Черкесск",
    "Республика Карелия": "Петрозаводск",
    "Республика Коми": "Сыктывкар",
    "Республика Крым": "Симферополь",
    "Республика Марий Эл": "Йошкар-Ола",
    "Республика Мордовия": "Саранск",
    "Республика Саха (Якутия)": "Якутск",
    "Республика Северная Осетия-Алания": "Владикавказ",
    "Республика Татарстан": "Казань",
    "Республика Тыва": "Кызыл",
    "Республика Удмуртская": "Ижевск",
    "Республика Хакасия": "Абакан",
    "Чеченская Республика": "Грозный",
    "Чувашская Республика": "Чебоксары",
    "Алтайский край": "Барнаул",
    "Забайкальский край": "Чита",
    "Камчатский край": "Петропавловск-Камчатский",
    "Краснодарский край": "Краснодар",
    "Красноярский край": "Красноярск",
    "Пермский край": "Пермь",
    "Приморский край": "Владивосток",
    "Ставропольский край": "Ставрополь",
    "Хабаровский край": "Хабаровск",
    "Амурская область": "Благовещенск",
    "Архангельская область": "Архангельск",
    "Астраханская область": "Астрахань",
    "Белгородская область": "Белгород",
    "Брянская область": "Брянск",
    "Владимирская область": "Владимир",
    "Волгоградская область": "Волгоград",
    "Вологодская область": "Вологда",
    "Воронежская область": "Воронеж",
    "Ивановская область": "Иваново",
    "Иркутская область": "Иркутск",
    "Калининградская область": "Калининград",
    "Калужская область": "Калуга",
    "Кемеровская область": "Кемерово",
    "Кировская область": "Киров",
    "Костромская область": "Кострома",
    "Курганская область": "Курган",
    "Курская область": "Курск",
    "Ленинградская область": "Санкт-Петербург",
    "Липецкая область": "Липецк",
    "Магаданская область": "Магадан",
    "Московская область": "Москва",
    "Мурманская область": "Мурманск",
    "Нижегородская область": "Нижний Новгород",
    "Новгородская область": "Великий Новгород",
    "Новосибирская область": "Новосибирск",
    "Омская область": "Омск",
    "Оренбургская область": "Оренбург",
    "Орловская область": "Орёл",
    "Пензенская область": "Пенза",
    "Псковская область": "Псков",
    "Ростовская область": "Ростов-на-Дону",
    "Рязанская область": "Рязань",
    "Самарская область": "Самара",
    "Саратовская область": "Саратов",
    "Сахалинская область": "Южно-Сахалинск",
    "Свердловская область": "Екатеринбург",
    "Смоленская область": "Смоленск",
    "Тамбовская область": "Тамбов",
    "Тверская область": "Тверь",
    "Томская область": "Томск",
    "Тульская область": "Тула",
    "Тюменская область": "Тюмень",
    "Ульяновская область": "Ульяновск",
    "Херсонская область": "Херсон",
    "Челябинская область": "Челябинск",
    "Ярославская область": "Ярославль",
    "Еврейская автономная область": "Биробиджан",
    "Ненецкий автономный округ": "Нарьян-Мар",
    "Ханты-Мансийский автономный округ": "Ханты-Мансийск",
    "Чукотский автономный округ": "Анадырь",
    "Ямало-Ненецкий автономный округ": "Салехард"}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Как хорошо ты знаешь Россиию?'
        res['response']['buttons'] = [
            {
                'title': 'Отлично!',
                'hide': True
            },
            {
                'title': 'Не знаю',
                'hide': True
            },
            {
                'title': 'Плохо',
                'hide': True
            }
        ]
        sessionStorage['game_started'] = False
        return

    if not sessionStorage['game_started']:
        if is_part_in_list(req['request']['original_utterance'].lower(), ["хорошо", "отлично", "великолепно", "шикарно"]):
            res['response']['text'] = 'Давай проверим?'
            return
        elif is_part_in_list(req['request']['original_utterance'].lower(), ["не", "плохо", "так себе", "ужасно"]):
            res['response']['text'] = 'Это исправимо!'
            return

        res['response']['text'] = 'Я буду называть субъекты, а ты должен будеш назвать их столицу. Начнем!'
        sessionStorage[user_id]['attempt'] = 1
        sessionStorage['game_started'] = True
        sessionStorage[user_id]['guessed_regions'] = []
        sessionStorage[user_id]['score'] = 0
    else:
        play_game(req, res)


def play_game(req, res):
    user_id = req['session']['user_id']
    attempt = sessionStorage[user_id]['attempt']
    if attempt == 1:
        if len(sessionStorage[user_id]['guessed_regions']) == len(regions):
            score = 82 * 3 / sessionStorage[user_id]['score'] * 100
            res['response']['text'] = f'На этом субъекты Российсой федерации закончились. Ты знаеш Россию на {score}%'
            sessionStorage['game_started'] = False
        reg = random.choice(list(regions))
        while reg in sessionStorage[user_id]['guessed_regions']:
            reg = random.choice(list(regions))
        sessionStorage[user_id]['reg'] = reg
        res['response']['text'] = reg
    else:
        reg = sessionStorage[user_id]['reg']
        if get_city(req) == regions[reg]:
            res['response']['text'] = 'Правильно!'
            sessionStorage[user_id]['guessed_cities'].append(reg)
            sessionStorage[user_id]['attempt'] = 1
            if attempt == 2:
                sessionStorage[user_id]['score'] += 2
            else:
                sessionStorage[user_id]['score'] += 1
            return
        else:
            if attempt == 3:
                res['response']['text'] = f'Вы пытались. Это {regions[reg]}.'
                sessionStorage[user_id]['guessed_cities'].append(reg)
                return
            else:
                res['response']['text'] = 'А вот и не угадал! Попробуй еще раз.'
    sessionStorage[user_id]['attempt'] += 1


def is_part_in_list(str_, words):
    for word in words:
        if word.lower() in str_.lower():
            return True
    return False


def get_city(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            return entity['value'].get('city', None)


if __name__ == '__main__':
    app.run()