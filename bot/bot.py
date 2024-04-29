import asyncio
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from API.news import get_top_news
import random
import joke

from configuration.config import TOKEN_TG

import keyboards as kb

from database.models import async_main
import database.requests as rq

base_city = ""
base_joke = ""
base_news = ""


TOKEN = TOKEN_TG

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Обработчики команд
@dp.message(Command("start"))
async def start_command_handler(message: Message) -> None:
    await command_start_handler(message)

@dp.message(Command("help"))
async def start_command_handler(message: Message) -> None:
    await help_command_handler(message)

@dp.message(Command("weather"))
async def weather_command_handler(message: Message) -> None:
    await command_weather_handler(message)

@dp.message(Command("news"))
async def news_command_handler(message: Message) -> None:
    await news_command_handler(message)

@dp.message(Command("joke"))
async def joke_command_handler(message: Message) -> None:
    await joke_main_menu_handler(message)

@dp.message(Command("settings"))
async def settings_command_handler(message: Message) -> None:
    await settings_handler(message)

@dp.message(Command("help"))
async def help_command_handler(message: Message) -> None:
    await help_handler(message)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global base_city, base_news, base_joke
    user_id = message.from_user.id
    base_city, base_news, base_joke = await rq.get_user_settings(user_id)
    await rq.set_user(message.from_user.id)
    await rq.set_base_city(message.from_user.id, base_city)  # Сохранить текущую команду
    await rq.set_base_news(message.from_user.id, base_news)  # Сохранить текущую команду
    await rq.set_base_joke(message.from_user.id, base_joke)  # Сохранить текущую команду
    await rq.set_current_command(message.from_user.id, "/start")  # Сохранить текущую команду
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!",
        reply_markup=kb.menu_keyboard
    )


# Функция для создания клавиатуры настроек
def create_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"Погода☀️: {base_city}")],
            [KeyboardButton(text=f"Новости📰: {kb.category_mapping_rus[base_news]}")],  # Используем словарь новостей
            [KeyboardButton(text=f"Шутки🤡: {kb.joke_category_mapping_rus[base_joke]}")],  # Используем словарь шуток
            [KeyboardButton(text="Меню↩️")]
        ],
        resize_keyboard=True
    )

# Группы состояний
class JokeStates(StatesGroup):
    waiting_for_category = State()

class NewsStates(StatesGroup):
    waiting_for_category = State()

class WeatherStates(StatesGroup):
    waiting_for_city = State()

class SettingsStates(StatesGroup):
    changing_default_weather = State()
    changing_default_news = State()
    changing_default_joke = State()

# Обработчик для нажатия кнопки "Шутка🤡" в основном меню
@dp.message(lambda message: message.text == "Шутка🤡")
async def joke_main_menu_handler(message: Message) -> None:
    global base_city, base_news, base_joke
    user_id = message.from_user.id
    base_city, base_news, base_joke = await rq.get_user_settings(user_id)
    await rq.set_current_command(message.from_user.id, "/joke")

    if base_joke.lower() == "работа":
        joke_to_tell = random.choice(joke.work_jokes)
    elif base_joke.lower() == "штирлиц":
        joke_to_tell = random.choice(joke.shtirlitz_jokes)
    elif base_joke.lower() == "undertale":
        joke_to_tell = random.choice(joke.undertale_jokes)
    elif base_joke.lower() == "программисты":
        joke_to_tell = random.choice(joke.programmer_jokes)
    else:
        joke_to_tell = "Категория шуток по умолчанию некорректна."

    await message.answer(joke_to_tell)
    await message.answer("Что дальше?", reply_markup=kb.joke_action_keyboard())


# Обработчик для выбора другой категории шуток
@dp.message(lambda message: message.text == "Другая категория🤡")
async def choose_another_joke_category(message: Message, state: FSMContext) -> None:
    await message.answer("Выберите новую категорию шуток:", reply_markup=kb.joke_categories_keyboard)
    await state.set_state(JokeStates.waiting_for_category)


# Обработчик для выбранной категории шуток
@dp.message(JokeStates.waiting_for_category)
async def tell_joke_from_selected_category(message: Message, state: FSMContext) -> None:
    selected_category = message.text

    if selected_category == "Работа💼":
        joke_to_tell = random.choice(joke.work_jokes)
    elif selected_category == "Штирлиц🤫":
        joke_to_tell = random.choice(joke.shtirlitz_jokes)
    elif selected_category == "Undertale👻":
        joke_to_tell = random.choice(joke.undertale_jokes)
    elif selected_category == "Программисты🧑‍💻":
        joke_to_tell = random.choice(joke.programmer_jokes)
    else:
        joke_to_tell = "Некорректная категория. Пожалуйста, выберите из доступных опций."

    await message.answer(joke_to_tell)
    await message.answer("Что дальше?", reply_markup=kb.joke_action_keyboard())
    await state.clear()


# Обработчик для "Меню↩️"
@dp.message(lambda message: message.text == "Меню↩️")
async def back_to_menu(message: Message) -> None:
    await rq.set_current_command(message.from_user.id, "/menu")
    await message.answer("Вы вернулись в меню.", reply_markup=kb.menu_keyboard)


# Обработчик для команды "/news"
@dp.message(lambda message: message.text == "Новости📰")
async def news_command_handler(message: Message) -> None:
    await rq.set_current_command(message.from_user.id, "/news")
    news_texts = get_top_news(base_news)

    for news_text in news_texts:

        await message.answer(news_text, parse_mode=ParseMode.MARKDOWN)

    await message.answer("Выберите другую категорию или вернитесь в меню:",
                         reply_markup=kb.single_row_keyboard)


# Обработчик для выбора другой категории
@dp.message(lambda message: message.text == "Другая категория📰")
async def choose_another_category(message: Message, state: FSMContext) -> None:
    await message.answer("Выберите категорию новостей:", reply_markup=kb.categories_keyboard)
    await state.set_state(NewsStates.waiting_for_category)

# Обработчик для получения новостей из выбранной категории
@dp.message(NewsStates.waiting_for_category)
async def get_news_from_category(message: Message, state: FSMContext) -> None:
    category = message.text
    category_in_english = kb.category_mapping.get(category, category)
    news_texts = get_top_news(category_in_english)
    for news_text in news_texts:
        await message.answer(news_text, parse_mode=ParseMode.MARKDOWN)

    await state.clear()
    await message.answer("Выберите другую категорию или вернитесь в меню:",
                         reply_markup=kb.single_row_keyboard)


# Добавим обработчик для команды "Помощь🤖"
@dp.message(lambda message: message.text == "Помощь🤖")
async def help_handler(message: Message) -> None:
    await rq.set_current_command(message.from_user.id, "/help")
    command_list = """
<b>Доступные команды:</b>
/start - Начать общение с ботом
/help - Помощь пользователю
/weather - Узнать погоду
/news - Получить новости
/joke - Узнать шутку
/settings - Открыть настройки
"""
    await message.answer(
        command_list,
        parse_mode=ParseMode.HTML,
        reply_markup=kb.help_keyboard
    )

# Добавим обработчик для "Написать в поддержку"
@dp.message(lambda message: message.text == "Написать в поддержку🆘")
async def contact_support(message: Message) -> None:
    support_link = "[@worm47](https://t.me/worm47)"
    await message.answer(
        f"Контакты поддержки: {support_link}",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


# Обработчик для "Настройки⚙️"
@dp.message(lambda message: message.text == "Настройки⚙️")
async def settings_handler(message: Message) -> None:
    global base_city, base_news, base_joke
    user_id = message.from_user.id
    base_city, base_news, base_joke = await rq.get_user_settings(user_id)
    await rq.set_current_command(message.from_user.id, "/setting")
    await message.answer(
        "Для изменения параметров по умолчанию, используйте меню:",
        reply_markup=create_settings_keyboard()
    )

# Обработчики для настройки параметров
@dp.message(lambda message: message.text.startswith("Погода☀️:"))
async def change_default_weather(message: Message, state: FSMContext) -> None:
    await message.answer("Введите новый базовый город:")
    await state.set_state(SettingsStates.changing_default_weather)

@dp.message(SettingsStates.changing_default_weather)
async def set_default_weather(message: Message, state: FSMContext) -> None:
    global base_city
    base_city = message.text
    await rq.set_base_city(message.from_user.id, base_city)
    await message.answer(f"Базовый город изменен на: {base_city}", reply_markup=create_settings_keyboard())
    await state.clear()


# Обработчик для изменения базовой категории новостей по умолчанию
@dp.message(lambda message: message.text.startswith("Новости📰:"))
async def change_default_news(message: Message, state: FSMContext) -> None:
    await message.answer("Выберите категорию новостей по умолчанию:", reply_markup=kb.categories_keyboard)
    await state.set_state(SettingsStates.changing_default_news)

# Обработчик состояния для установки новой базовой категории новостей
@dp.message(SettingsStates.changing_default_news)
async def set_default_news(message: Message, state: FSMContext) -> None:
    global base_news
    category_in_english = list(kb.category_mapping_rus.keys())[list(kb.category_mapping_rus.values()).index(message.text)]
    if category_in_english:
        base_news = category_in_english
        await rq.set_base_news(message.from_user.id, base_news)
        await message.answer(f"Категория новостей по умолчанию изменена на: {kb.category_mapping_rus[base_news]}",
                             reply_markup=create_settings_keyboard())
    else:
        await message.answer("Неправильный выбор категории. Пожалуйста, выберите из предложенных.",
                             reply_markup=kb.categories_keyboard)
    await state.clear()


# Обработчик изменения базовой категории шуток по умолчанию
@dp.message(lambda message: message.text.startswith("Шутки🤡:"))
async def change_default_joke_request(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите новую базовую категорию шуток:",
        reply_markup=kb.joke_categories_keyboard
    )
    await state.set_state(SettingsStates.changing_default_joke)

# Обработчик для установки новой базовой категории шуток
@dp.message(SettingsStates.changing_default_joke)
async def set_default_joke(message: Message, state: FSMContext) -> None:
    global base_joke
    selected_category = list(kb.joke_category_mapping_rus.keys())[list(kb.joke_category_mapping_rus.values()).index(message.text)]

    if selected_category:
        base_joke = selected_category
        await rq.set_base_joke(message.from_user.id, base_joke)
        await message.answer(
            f"Базовая категория шуток изменена на: {kb.joke_category_mapping_rus[base_joke]}",
            reply_markup=create_settings_keyboard()
        )
    else:
        await message.answer(
            "Некорректный выбор. Пожалуйста, выберите из доступных категорий.",
            reply_markup=kb.joke_categories_keyboard
        )

    await state.clear()

# Обработчик для "Погода☀️"
@dp.message(lambda message: message.text == "Погода☀️")
async def command_weather_handler(message: Message) -> None:
    global base_city, base_news, base_joke
    user_id = message.from_user.id
    base_city, base_news, base_joke = await rq.get_user_settings(user_id)
    await rq.set_current_command(message.from_user.id, "/weather")
    from API.weather import get_weather

    weather_info = get_weather(base_city)

    if weather_info != "Возможно, вы ввели несуществующий город✍️":

        await message.answer(weather_info, reply_markup=kb.weather_action_keyboard)
    else:
        await message.answer("Некорректный город по умолчанию🛠", reply_markup=kb.weather_action_keyboard)

# Обработчик для "Другой город🌍"
@dp.message(lambda message: message.text == "Другой город🌍")
async def choose_another_city(message: Message, state: FSMContext) -> None:
    await message.answer("Введите название города для прогноза погоды:")
    await state.set_state(WeatherStates.waiting_for_city)

# Обработчик для ответа на запрос о городе
@dp.message(WeatherStates.waiting_for_city)
async def get_weather_for_city(message: Message, state: FSMContext) -> None:
    city_name = message.text
    from API.weather import get_weather
    weather_info = get_weather(city_name)
    await message.answer(weather_info, reply_markup=kb.weather_action_keyboard)
    await state.clear()

# Универсальный обработчик для других команд
@dp.message()
async def handle_messages(message: Message) -> None:
    response = {
    }.get(message.text, "Неизвестная команда.")

    await message.answer(response, reply_markup=kb.menu_keyboard)

# Запуск бота
async def main() -> None:
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

