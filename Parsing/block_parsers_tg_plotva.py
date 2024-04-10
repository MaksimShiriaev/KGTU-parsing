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

class Telegram_parser_plotva():
    
    # URL страницы канала Telegram
    channel_url = "https://t.me/s/ligaplotv"

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
    news_urls = []

    # Итерируемся по всем постам и добавляем их в список
    # Создаем пустое множество для хранения уникальных новостей
    unique_news = []
    # Итерируемся по всем постам и добавляем их в список
    for post, time, url in zip(posts, times, urls):
        post_text = post.text.strip()
        time_text = time.text.strip()
        image_links = [img["src"] for img in post.find_all("img")]
        
        # Создаем кортеж с текстом новости и ссылками на картинки
        news_info = (post_text, image_links)
        
        # Проверяем, что комбинация текста и ссылок на картинки уникальна
        if news_info not in unique_news:
            unique_news.append(news_info)
            news_data.append(post_text)
            post_time.append(time_text)
            news_urls.append(url)
            
    parsing_date = str(date.today())
        
    title = [sent_tokenize(news)[0] for news in news_data]


    # Создаем DataFrame из списка новостей
    df = pd.DataFrame({'url': news_urls,'topic_block': 'tg_plotva', 'parsing_date': parsing_date, 'public_date': post_time, 'title': title, 'context': unique_news, 'html': str(html)})
