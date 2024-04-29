from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def joke_action_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Другая категория🤡"), KeyboardButton(text="Меню↩️")]
        ],
        resize_keyboard=True
    )

joke_categories_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Работа💼"), KeyboardButton(text="Штирлиц🤫")],
        [KeyboardButton(text="Undertale👻"), KeyboardButton(text="Программисты🧑‍💻")]
    ],
    resize_keyboard=True
)

category_mapping_rus = {
    "business": "Бизнес💰",
    "entertainment": "Развлечения🎮",
    "health": "Здоровье💊",
    "science": "Наука🧬",
    "sports": "Спорт🏐",
    "technology": "Технологии💻"
}

category_mapping = {
    "Бизнес💰": "business",
    "Развлечения🎮": "entertainment",
    "Здоровье💊": "health",
    "Наука🧬": "science",
    "Спорт🏐": "sports",
    "Технологии💻": "technology"
}

joke_category_mapping_rus = {
    "работа": "Работа💼",
    "штирлиц": "Штирлиц🤫",
    "undertale": "Undertale👻",
    "программисты": "Программисты🧑‍💻"
}


categories_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=category_mapping_rus["business"]), KeyboardButton(text=category_mapping_rus["entertainment"])],
        [KeyboardButton(text=category_mapping_rus["health"]), KeyboardButton(text=category_mapping_rus["science"])],
        [KeyboardButton(text=category_mapping_rus["sports"]), KeyboardButton(text=category_mapping_rus["technology"])]
    ],
    resize_keyboard=True
)

menu_buttons = [
    [KeyboardButton(text="Новости📰"), KeyboardButton(text="Погода☀️"), KeyboardButton(text="Шутка🤡")],  # Первый ряд
    [KeyboardButton(text="Помощь🤖"), KeyboardButton(text="Настройки⚙️")]  # Второй ряд
]
menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)


weather_action_buttons = [
    [KeyboardButton(text="Другой город🌍"), KeyboardButton(text="Меню↩️")]
]
weather_action_keyboard = ReplyKeyboardMarkup(keyboard=weather_action_buttons, resize_keyboard=True)


single_row_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Другая категория📰"), KeyboardButton(text="Меню↩️")]
    ],
    resize_keyboard=True
)


help_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Написать в поддержку🆘"), KeyboardButton(text="Меню↩️")],
    ],
    resize_keyboard=True
)
