import requests
from configuration.config import API_KEY_NEWS

# Ключ API
API_KEY = API_KEY_NEWS

# Базовый URL для запросов к News API
BASE_URL = 'https://newsapi.org/v2/top-headlines'

def get_top_news(category, country='ru', number_of_articles=4):

    params = {
        'category': category,
        'country': country,
        'apiKey': API_KEY,
        'pageSize': number_of_articles
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return [f"Ошибка при запросе данных: {response.status_code}"]

    data = response.json()
    articles = data.get('articles', [])
    messages = []

    for article in articles:
        title = article.get('title', 'Нет заголовка')
        url = article.get('url', '#')
        message = f"{title}\n[ссылка]({url})"
        messages.append(message)

    return messages
