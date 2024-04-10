import re
import os
import time
import random
import requests


from datetime import datetime
from bs4 import BeautifulSoup
from base_parser import BaseParser

month_replacements = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}

#Парсинг блока https://www.klgtu.ru/abitur/
class Edu_programms_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/abitur/'
        self.pages = ['op', 'op-mag'] #Здесь страницы уже в виде списка
        self.time_sleep = time_sleep 
        self.topic_block = 'edu_programms'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        for page in self.pages: 
            cur_url = self.url + page + '?view=table'
            src = self.read_site(cur_url)
            soup = BeautifulSoup(src, "lxml")
            one_page_urls = [item.get("href") for item in \
                    soup.find_all("a", class_="article-program article-program--light")]
            all_pages_urls.extend(one_page_urls)

            if self.time_sleep is True:
                time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = None
        headline_info = ",".join([item.text for item in soup.find_all(class_="program-headline__info")]) + "; "
        apply_conditions = ", ".join([item.text for item in soup.find_all("div", class_="program-stats__group")]) + ". "

        block_title = 'None'
        block_text = soup.find_all("div", class_= "block-info mb-15")
        block_content = 'None'

        html = soup.find('main')
        
        res = headline_info + apply_conditions + block_content
        res = self.regex_cleaning(res)

        public_date = None
        title = block_title

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return block_title, res, public_date, str(html)




#Парсинг блока https://www.klgtu.ru/media/novosti/
class Kgtu_news_parser(BaseParser):
    def __init__(self, pages, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/media/novosti/'
        self.pages = pages + 1
        self.time_sleep = time_sleep
        self.topic_block = 'news'
        self.min_text_size = 400

    #Сбор ссылок на вопросы с главной страницы
    def parse_urls(self):
        all_pages_urls = []
        cur_url = self.url
        for i in range(2, self.pages + 1):
            src = self.read_site(cur_url)
            soup = BeautifulSoup(src, "lxml")
            one_page_urls = [item.get("href") for item in \
                             soup.find_all("a", class_="article-news")]
            all_pages_urls.extend(one_page_urls)
            cur_url = self.url + f'?PAGEN_1={i}'
            if self.time_sleep is True:
                time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов c ответами на вопросы
    def parse_text(self, url):
        cur_url = url
        src = self.read_site(cur_url)
        soup = BeautifulSoup(src, "lxml")

        date = soup.find("time", class_="toolbar-post__text mbm-10").text.replace("\n", " ")
        for russian_month, numeric_month in month_replacements.items():
            if russian_month in date:
                date_str = date.replace(russian_month, numeric_month).strip()
        # Преобразование строки в объект datetime
        date_obj = datetime.strptime(date_str, '%d %m %Y %H:%M')
        # Преобразование объекта datetime в строку в нужном формате
        formatted_date = date_obj.strftime('%Y-%m-%d')

        header = soup.find("h1", class_="title title--large mb-40 mbm-15").text.replace("\n", " ")

        news_text = " ".join([item.text.strip() for item in soup.find_all("div", class_="editor editor--14 mb-30 mbm-15")])#.replace("\n", "")
        paragraphs = [paragraph.strip() for paragraph in news_text.split('\n') if paragraph.strip()]
        news = ";;".join(paragraphs)
        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html)




#Парсинг блока https://www.klgtu.ru/media/anonsy/
class Kgtu_anons_parser(BaseParser):
    def __init__(self, pages, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/media/anonsy/'
        self.pages = pages + 1
        self.time_sleep = time_sleep
        self.topic_block = 'anons'
        self.min_text_size = 400

    #Сбор ссылок на вопросы с главной страницы
    def parse_urls(self):
        all_pages_urls = []
        cur_url = self.url
        for i in range(2, self.pages + 1):
            src = self.read_site(cur_url)
            soup = BeautifulSoup(src, "lxml")
            one_page_urls = [item.get("href") for item in \
                             soup.find_all("a", class_="article-announcement")]
            all_pages_urls.extend(one_page_urls)
            cur_url = self.url + f'?PAGEN_1={i}'
            if self.time_sleep is True:
                time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов c ответами на вопросы
    def parse_text(self, url):
        cur_url = url
        src = self.read_site(cur_url)
        soup = BeautifulSoup(src, "lxml")

        date = soup.find("time", class_="toolbar-post__text mbm-10").text.replace("\n", " ")
        for russian_month, numeric_month in month_replacements.items():
            if russian_month in date:
                date_str = date.replace(russian_month, numeric_month).strip()
        # Преобразование строки в объект datetime
        date_obj = datetime.strptime(date_str, '%d %m %Y %H:%M')
        # Преобразование объекта datetime в строку в нужном формате
        formatted_date = date_obj.strftime('%Y-%m-%d')

        header = soup.find("h1", class_="title title--large mb-40 mbm-15").text.replace("\n", " ")

        news_text = " ".join([item.text.strip() for item in soup.find_all("div", class_="editor editor--14 mb-30 mbm-15")])#.replace("\n", "")
        paragraphs = [paragraph.strip() for paragraph in news_text.split('\n') if paragraph.strip()]
        news = ";;".join(paragraphs)

        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html)




#Парсинг блока https://www.klgtu.ru/media/obyavleniya/
class Kgtu_obyava_parser(BaseParser):
    def __init__(self, pages, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/media/obyavleniya/'
        self.pages = pages + 1
        self.time_sleep = time_sleep
        self.topic_block = 'obyava'
        self.min_text_size = 400

    #Сбор ссылок на вопросы с главной страницы
    def parse_urls(self):
        all_pages_urls = []
        cur_url = self.url
        for i in range(2, self.pages + 1):
            src = self.read_site(cur_url)
            soup = BeautifulSoup(src, "lxml")
            one_page_urls = [item.get("href") for item in \
                             soup.find_all("a", class_="article-media")]
            all_pages_urls.extend(one_page_urls)
            cur_url = self.url + f'?PAGEN_1={i}'
            if self.time_sleep is True:
                time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов c ответами на вопросы
    def parse_text(self, url):
        cur_url = url
        src = self.read_site(cur_url)
        soup = BeautifulSoup(src, "lxml")

        date = soup.find("time", class_="toolbar-post__text mbm-10").text.replace("\n", " ")
        for russian_month, numeric_month in month_replacements.items():
            if russian_month in date:
                date_str = date.replace(russian_month, numeric_month).strip()
        # Преобразование строки в объект datetime
        date_obj = datetime.strptime(date_str, '%d %m %Y %H:%M')
        # Преобразование объекта datetime в строку в нужном формате
        formatted_date = date_obj.strftime('%Y-%m-%d')

        header = soup.find("h1", class_="title title--large mb-40 mbm-15").text.replace("\n", " ")

        news_text = " ".join([item.text.strip() for item in soup.find_all("div", class_="editor editor--14 mb-30 mbm-15")])#.replace("\n", "")
        paragraphs = [paragraph.strip() for paragraph in news_text.split('\n') if paragraph.strip()]
        news = ";;".join(paragraphs)

        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html)




#Парсинг блока https://www.klgtu.ru/divisions/studencheskiy_gorodok/
class Kgtu_studgorodok_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/divisions/studencheskiy_gorodok/'
        self.time_sleep = time_sleep 
        self.topic_block = 'studgorodok'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []

        cur_url = self.url + '?view=table'
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls_1 = [item.get("href") for item in \
                soup.find_all("a", class_="link-download mb-20 mbm-15")]
        one_page_urls_2 = [item.get("href") for item in \
                soup.find_all("a", class_="link-download mb-40 mbm-25")]
        all_pages_urls.extend(one_page_urls_1)
        all_pages_urls.extend(one_page_urls_2)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = None
        headline_info = ",".join([item.text for item in soup.find_all(class_="program-headline__info")]) + "; "
        apply_conditions = ", ".join([item.text for item in soup.find_all("div", class_="program-stats__group")]) + ". "

        block_title = 'None'
        block_text = soup.find_all("div", class_= "block-info mb-15")
        block_content = 'None'

        html = soup.find('main')
        
        res = headline_info + apply_conditions + block_content
        res = self.regex_cleaning(res)

        public_date = None
        title = block_title

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return block_title, res, public_date, str(html)




#Парсинг блока https://klgtu.ru/divisions/tsentr_professionalnogo_razvitiya_i_karery/
class Kgtu_praktika_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/divisions/tsentr_professionalnogo_razvitiya_i_karery/'
        self.time_sleep = time_sleep 
        self.topic_block = 'praktika'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []

        cur_url = self.url + '?view=table'
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls_1 = [item.get("href") for item in \
                soup.find_all("a", class_="link-download mb-20 mbm-15")]
        one_page_urls_2 = [item.get("href") for item in \
                soup.find_all("a", class_="link-download mb-40 mbm-25")]
        all_pages_urls.extend(one_page_urls_1)
        all_pages_urls.extend(one_page_urls_2)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = None
        headline_info = ",".join([item.text for item in soup.find_all(class_="program-headline__info")]) + "; "
        apply_conditions = ", ".join([item.text for item in soup.find_all("div", class_="program-stats__group")]) + ". "

        block_title = 'None'
        block_text = soup.find_all("div", class_= "block-info mb-15")
        block_content = 'None'

        html = soup.find('main')
        
        res = headline_info + apply_conditions + block_content
        res = self.regex_cleaning(res)

        public_date = None
        title = block_title

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return block_title, res, public_date, str(html)




#Парсинг блока https://klgtu.ru/institutes/
class Kgtu_instituts_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/'
        self.pages = ['institut_rybolovstva_i_akvakultury'] #Здесь страницы уже в виде списка
        self.time_sleep = time_sleep 
        self.topic_block = 'instituts'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-card")]
        all_pages_urls.extend(one_page_urls)
        #print(all_pages_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("div", class_="block-accent block-accent--36").text.replace("\n", " ")
        date = 'None'
        news_1 = " ".join([item.text.strip() for item in soup.find_all("div", class_="wrapper wrapper--45-40 wrapper--grey-light wrapper--radius wrapper--mob-0-0")])#.replace("\n", ";;")
        news_2 = " ".join([item.text.strip() for item in soup.find_all("div", class_="wrapper wrapper--45-40 wrapper--mob-0-0")])#.replace("\n", ";;")
        news_3 = " ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--4")])#.replace("\n", "")

        news = ";;".join([news_1, news_2, news_3]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html)




#Парсинг блока https://www.klgtu.ru/en/media/news_en/
class Kgtu_news_en_parser(BaseParser):
    def __init__(self, pages, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/en/media/news_en/'
        self.pages = pages + 1
        self.time_sleep = time_sleep
        self.topic_block = 'news_en'
        self.min_text_size = 400

    #Сбор ссылок на вопросы с главной страницы
    def parse_urls(self):
        all_pages_urls = []
        cur_url = self.url
        for i in range(2, self.pages + 1):
            src = self.read_site(cur_url)
            soup = BeautifulSoup(src, "lxml")
            one_page_urls = [item.get("href") for item in \
                             soup.find_all("a", class_="article-news")]
            all_pages_urls.extend(one_page_urls)
            cur_url = self.url + f'?PAGEN_1={i}'
            if self.time_sleep is True:
                time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов c ответами на вопросы
    def parse_text(self, url):
        cur_url = url
        src = self.read_site(cur_url)
        soup = BeautifulSoup(src, "lxml")

        date = soup.find("time", class_="toolbar-post__text mbm-10").text.replace("\n", " ")
        for russian_month, numeric_month in month_replacements.items():
            if russian_month in date:
                date_str = date.replace(russian_month, numeric_month).strip()
        # Преобразование строки в объект datetime
        date_obj = datetime.strptime(date_str, '%d %m %Y %H:%M')
        # Преобразование объекта datetime в строку в нужном формате
        formatted_date = date_obj.strftime('%Y-%m-%d')

        header = soup.find("h1", class_="title title--large mb-40 mbm-15").text.replace("\n", " ")

        news_text = " ".join([item.text.strip() for item in soup.find_all("div", class_="editor editor--14 mb-30 mbm-15")])#.replace("\n", "")
        paragraphs = [paragraph.strip() for paragraph in news_text.split('\n') if paragraph.strip()]
        news = ";;".join(paragraphs)

        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html)




#Парсинг блока https://www.klgtu.ru/en/applicants/
class Edu_programms_en_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://www.klgtu.ru/en/applicants/'
        self.pages = ['op', 'op-mag'] #Здесь страницы уже в виде списка
        self.time_sleep = time_sleep 
        self.topic_block = 'edu_programms_en'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []

        for page in self.pages: 
            cur_url = self.url + page + '?view=table'
            src = self.read_site(cur_url)
            soup = BeautifulSoup(src, "lxml")
            one_page_urls = [item.get("href") for item in \
                    soup.find_all("a", class_="article-program article-program--light")]
            all_pages_urls.extend(one_page_urls)

            if self.time_sleep is True:
                time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = None
        headline_info = ",".join([item.text for item in soup.find_all(class_="program-headline__info")]) + "; "
        apply_conditions = ", ".join([item.text for item in soup.find_all("div", class_="program-stats__group")]) + ". "

        block_title = 'None'
        block_text = soup.find_all("div", class_= "block-info mb-15")
        block_content = 'None'

        html = soup.find('main')
        
        res = headline_info + apply_conditions + block_content
        res = self.regex_cleaning(res)

        public_date = None
        title = block_title

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return block_title, res, public_date, str(html)
    
