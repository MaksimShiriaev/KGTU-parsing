import os
import pandas as pd

from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, update

#Функция для парсинга данных
def parse_data(parser):
    parsed_urls = parser.parse_urls()
    new_urls = []
    new_texts = []
    new_titles = []
    new_public_dates = []
    new_html = []
    for url in parsed_urls:
        title, text, public_date, html = parser.parse_text(url)
        if text is not None:
            new_urls.append(url)
            new_texts.append(text)  
            new_titles.append(title)    
            new_public_dates.append(public_date)
            new_html.append(html)

    parsing_date = str(date.today())
    new_df = pd.DataFrame({'url': new_urls, 'topic_block': parser.topic_block, 'parsing_date': parsing_date, 'public_date': new_public_dates, 'title': new_titles, 'context': new_texts, "html": new_html})
    print(f"Cпарсено {len(new_df)} документов")
    return new_df

#функции ниже просто для ознакомления, их использовать не нужно

#Загрузка всех данных с таблицы table_name
def load_table(table_name, database_name):
    engine = create_engine(f'postgresql://......./{database_name}')
    all_data_query = f'SELECT * FROM {table_name}'
    df = pd.read_sql_query(all_data_query, engine)
    try:
        df.drop(columns=['index'], inplace=True)  
    except Exception:
        pass 
    return df


#Парсинг данных с учетом текущей информации в БД (это можно не использовать)
def parse_new_data(parser, table_name, database_name, replace = False):
    engine = create_engine(f'postgresql://......./{database_name}')
    all_urls_query = f'SELECT url FROM {table_name}'
    all_urls_df = pd.read_sql_query(all_urls_query, engine)
    
    #Множество существующих ссылок
    existing_raw_urls_set = set(all_urls_df['url'])
    #Ссылки на сайты, которые были спарсены
    parsed_urls = parser.parse_urls()

    new_urls = []
    new_texts = []
    new_titles = []
    new_public_dates = []

    update_urls = []
    update_texts = []
    update_titles = []
    update_public_dates = []
    for url in parsed_urls:
        #Если новые ссылки и не дублируются, добавляем в список новых
        if (url not in existing_raw_urls_set) and (url not in new_urls):
            title, text, public_date = parser.parse_text(url)
            if text is not None:
                new_urls.append(url)
                new_texts.append(text)  
                new_titles.append(title)    
                new_public_dates.append(public_date) 
        else:
            #иначе – в список для обновления
            if (replace is True) and (url not in update_urls):
                title, text, public_date = parser.parse_text(url)
                if text is not None:
                    update_urls.append(url)
                    update_texts.append(text) 
                    update_titles.append(title)
                    update_public_dates.append(public_date)

    parsing_date = str(date.today())
    new_df = pd.DataFrame({'url': new_urls, 'topic_block': parser.topic_block, 'parsing_date': parsing_date, 'public_date': new_public_dates, 'title': new_titles, 'context': new_texts})
    update_df = pd.DataFrame({'url': update_urls, 'topic_block': parser.topic_block, 'parsing_date': parsing_date, 'public_date': update_public_dates, 'title': update_titles, 'context': update_texts})
    print(f"Cпарсено {len(new_df)} новых документов и {len(update_df)} существующих документов")
    return new_df, update_df


#Сохранение спарсенных данных в БД
def save_parsed_data(new_df, update_df, table_name, database_name):
    engine = create_engine(f"postgresql://......./{database_name}")
    #Столбцы с новыми данными
    new_url = new_df['url'].tolist() 
    new_topic_block = new_df['topic_block'].tolist()
    new_parsing_date = new_df['parsing_date'].tolist()
    new_public_date = new_df['public_date'].tolist()
    new_title = new_df['title'].tolist() 
    new_context = new_df['context'].tolist() 
    #Столбцы с обновляемыми данными
    update_url = update_df['url'].tolist() 
    update_topic_block = update_df['topic_block'].tolist()
    update_parsing_date = update_df['parsing_date'].tolist()
    update_public_date = update_df['public_date'].tolist()
    update_title = update_df['title'].tolist()
    update_context = update_df['context'].tolist()

    #Сохранение новых сайтов и их содержимого в БД
    with Session(engine) as session:
        new_rows = [table_name(url = new_url[i],
                               topic_block = new_topic_block[i],
                               parsing_date = new_parsing_date[i],
                               public_date = new_public_date[i],
                               title = new_title[i],
                               context = new_context[i]) for i in range(len(new_url))]
        session.add_all(new_rows)
        session.commit()

    #Обновление существующих сайтов и их содержимого в БД
    with Session(engine) as session:
        update_rows = [{"url": update_url[i],
                        "topic_block": update_topic_block[i],
                        "parsing_date": update_parsing_date[i],
                        "public_date": update_public_date[i], 
                        "title": update_title[i],
                        "context": update_context[i]} for i in range(len(update_url))]
        session.execute(update(table_name), update_rows)
        session.commit()

    print(f"Добавлено {len(new_rows)} новых документов. Обновлено {len(update_rows)}  документов")






