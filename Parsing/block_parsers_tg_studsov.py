import re
import os
import time
import random
import requests
import pandas as pd
import nltk

from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
from base_parser import BaseParser
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

class Telegram_parser_studsov():
    # URL страницы канала Telegram
    channel_url = "https://t.me/s/students_counsil"

    # Получение HTML-кода страницы
    response = requests.get(channel_url)
    html_content = response.text

    # Создание объекта BeautifulSoup для разбора HTML-кода
    soup = BeautifulSoup(html_content, 'html.parser')

    # Нахождение всех элементов, содержащих текст постов
    posts = soup.find_all('div', class_='tgme_widget_message_text')
    times = soup.find_all('time', class_="time")
    urls = [item.get("href") for item in \
                        soup.find_all("a", class_="tgme_widget_message_date")]
    html = soup.find('main')

    # Создаем пустой список для хранения новостей
    news_data = []
    post_time = []

    # Итерируемся по всем постам и добавляем их в список
    for post, time in zip(posts, times):
        post_text = post.text.strip()
        time_text = time.text.strip()
        if post_text not in news_data:  # Проверяем, что пост еще не добавлен в список
            news_data.append(post_text)
            post_time.append(time_text)

    parsing_date = str(date.today())
        
    title = [sent_tokenize(news)[0] for news in news_data]


    # Создаем DataFrame из списка новостей
    df = pd.DataFrame({'url': urls,'topic_block': 'tg_studsov', 'parsing_date': parsing_date, 'public_date': post_time, 'title': title, 'context': news_data, 'html': str(html)})
