import requests
from configuration.config import API_KEY_WEATHER

# Ключ API от WeatherAPI
API_KEY = API_KEY_WEATHER

# URL для запросов к WeatherAPI
BASE_URL = 'http://api.weatherapi.com/v1'


def get_weather(city_name):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city_name}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        location = weather_data['location']['name']
        country = weather_data['location']['country']
        temperature_c = weather_data['current']['temp_c']
        wind_kph = weather_data['current']['wind_kph']
        humidity = weather_data['current']['humidity']

        weather_info = (
            f"Погода в {location}, {country}:\n"
            f"Температура: {temperature_c}°C\n"
            f"Скорость ветра: {wind_kph} км/ч\n"
            f"Влажность: {humidity}%"
        )

        return weather_info
    else:
        return "Возможно, вы ввели несуществующий город✍️"