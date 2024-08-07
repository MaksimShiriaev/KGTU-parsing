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
        news = " ;; ".join(paragraphs)
        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        parser_id = 'Kgtu_news_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




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
        news = " ;; ".join(paragraphs)

        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        parser_id = 'Kgtu_anons_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




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
        news = " ;; ".join(paragraphs)

        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        parser_id = 'Kgtu_obyava_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/institutes/
class Kgtu_instituts_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/'
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

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="wrapper wrapper--45-40 wrapper--grey-light wrapper--radius wrapper--mob-0-0")]).replace("\n\n\n\n", ";")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="wrapper wrapper--45-40 wrapper--mob-0-0")]).replace("\n\n\n\n", ";")
        news_3 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--4")])

        news = ". ;; ".join([news_1, news_2, news_3]).strip().replace("Контакты", "Контакты:").replace("email", "email -").replace("адрес", "адрес -")

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_instituts_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/divisions/rektorat/
class Kgtu_rektorat_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/divisions/rektorat/'
        self.time_sleep = time_sleep 
        self.topic_block = 'rektorat'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://klgtu.ru/divisions/rektorat/']
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="editor mb-50 mbm-20 upper")])
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", ";").replace(";;", ";").replace(";;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_rektorat_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/divisions/uchyenyy_sovet/
class Kgtu_uchyenyy_sovet_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/divisions/uchyenyy_sovet/'
        self.time_sleep = time_sleep 
        self.topic_block = 'uchyenyy_sovet'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://klgtu.ru/divisions/uchyenyy_sovet/']
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", ";").replace(";;", ";").replace(";;", ". ;;")

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_uchyenyy_sovet_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document

    


#Парсинг блока https://klgtu.ru/institutes/institut_rybolovstva_i_akvakultury/
class Kgtu_kafedra_rybolovstvo_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/institut_rybolovstva_i_akvakultury/'
        self.time_sleep = time_sleep 
        self.topic_block = 'kafedra_rybolovstvo'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-factoid article-factoid--line")]
        all_pages_urls.extend(one_page_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", ". ;;")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="block-drop__main")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", ". ;;").replace("; ;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_kafedra_rybolovstvo_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/institutes/institut_agroinzhenerii_i_pishchevykh_sistem/
class Kgtu_kafedra_agroinzheneria_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/institut_agroinzhenerii_i_pishchevykh_sistem/'
        self.time_sleep = time_sleep 
        self.topic_block = 'kafedra_agroinzheneria'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-factoid article-factoid--line")]
        all_pages_urls.extend(one_page_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", ". ;;")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="block-drop__main")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", " ;;").replace("; ;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_kafedra_agroinzheneria_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/institutes/institut_tsifrovykh_tekhnologiy/
class Kgtu_kafedra_icht_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/institut_tsifrovykh_tekhnologiy/'
        self.time_sleep = time_sleep 
        self.topic_block = 'kafedra_icht'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-factoid article-factoid--line")]
        all_pages_urls.extend(one_page_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", ". ;;")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="block-drop__main")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", " ;;").replace("; ;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_kafedra_icht_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/institutes/institut_morskikh_tekhnologiy_energetiki_i_stroitelstva/
class Kgtu_kafedra_energetika_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/institut_morskikh_tekhnologiy_energetiki_i_stroitelstva/'
        self.time_sleep = time_sleep 
        self.topic_block = 'kafedra_energetika'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-factoid article-factoid--line")]
        all_pages_urls.extend(one_page_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", ". ;;")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="block-drop__main")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", " ;;").replace("; ;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_kafedra_energetika_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/institutes/institut_otraslevoy_ekonomiki_i_upravleniya/
class Kgtu_kafedra_ekonomika_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/institutes/institut_otraslevoy_ekonomiki_i_upravleniya/'
        self.time_sleep = time_sleep 
        self.topic_block = 'kafedra_ekonomika'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-factoid article-factoid--line")]
        all_pages_urls.extend(one_page_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", ". ;;")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="block-drop__main")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", " ;;").replace("; ;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_kafedra_ekonomika_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/divisions/tsentr_preduniversitetskikh_proektov/
class Kgtu_predproekt_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/divisions/tsentr_preduniversitetskikh_proektov/'
        self.time_sleep = time_sleep 
        self.topic_block = 'predproekt'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://klgtu.ru/divisions/tsentr_preduniversitetskikh_proektov/']
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--4 order-m-2")]).replace("\n\n\n\n\n", " ;").replace(";;", ";").replace(";;", ". ;;").replace("номер телефона", "тел:").replace("email", "email:").replace("адрес", "адрес:")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", ";").replace(";;", ";").replace(";;", ". ;;")

        news = ". ;; ".join([news_1, news_2]).strip()

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_predproekt_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/divisions/upravlenie_nauchno_issledovatelskoy_deyatelnosti/
class Kgtu_science_explorer_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/divisions/upravlenie_nauchno_issledovatelskoy_deyatelnosti/'
        self.time_sleep = time_sleep 
        self.topic_block = 'science_explorer'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://klgtu.ru/divisions/upravlenie_nauchno_issledovatelskoy_deyatelnosti/']
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", ";").replace(";;", ";").replace(";;", ". ;;")

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_science_explorer_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/divisions/upravlenie_nauchno_issledovatelskoy_deyatelnosti/
class Kgtu_science_explorer_otdel_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/divisions/upravlenie_nauchno_issledovatelskoy_deyatelnosti/'
        self.time_sleep = time_sleep 
        self.topic_block = 'science_explorer_otdel'

    #Сбор ссылок с главной страницы раздела
    def parse_urls(self):
        all_pages_urls = []
        src = self.read_site(self.url)
        soup = BeautifulSoup(src, "lxml")
        one_page_urls = [item.get("href") for item in \
                soup.find_all("a", class_="article-factoid article-factoid--line")]
        all_pages_urls.extend(one_page_urls)

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))

        res = ['https://www.klgtu.ru' + url for url in all_pages_urls]
        return res

    #Парсинг текста сайтов
    def parse_text(self, url):
        news = ""
        src = self.read_site(url)
        soup = BeautifulSoup(src, "lxml")

        header = soup.find("h1", class_="title title--large mb-60 mbm-20").text.replace("\n", " ")
        date = 'None'

        news = "; ".join([item.text.strip() for item in soup.find_all("div", class_="columns__col columns__col--8 order-m-1 mbm-40")]).replace("\n\n\n\n\n", " ;").replace("; ;", ";").replace(";;", " ;;").replace("; ;", ". ;;")

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_science_explorer_otdel_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




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
        news = " ;; ".join(paragraphs)

        html = soup.find('main')

        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = formatted_date

        parser_id = 'Kgtu_news_en_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document




#Парсинг блока https://klgtu.ru/en/institutes/
class Kgtu_instituts_en_parser(BaseParser):
    def __init__(self, time_sleep=False):
        super().__init__()
        self.url = 'https://klgtu.ru/en/institutes/'
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

        news_1 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="wrapper wrapper--45-40 wrapper--grey-light wrapper--radius wrapper--mob-0-0")]).replace("\n\n\n\n", ";")
        news_2 = "; ".join([item.text.strip() for item in soup.find_all("div", class_="wrapper wrapper--45-40 wrapper--mob-0-0")]).replace("\n\n\n\n", ";")

        news = ". ;; ".join([news_1, news_2]).strip().replace("Contacts", "Contacts:").replace("phone", "phone -").replace("email", "email -").replace("address", "address -")

        html = soup.find('main')
        
        res = header + self.headers_sep + news
        res = self.regex_cleaning(res)
    
        public_date = date

        parser_id = 'Kgtu_instituts_en_parser'

        source = 'site'

        is_document = False

        if self.time_sleep is True:
            time.sleep(random.randrange(1, 3))
        return header, res, public_date, str(html), parser_id, source, is_document


    
