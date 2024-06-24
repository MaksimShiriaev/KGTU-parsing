import json

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Text, Date, Boolean
from sqlalchemy import create_engine

with open('parsing_settings.json') as file:
    settings = json.load(file)
UNI_NAME = settings['uni_name']
DB_NAME = settings['db_name']

class Base(DeclarativeBase):
    pass

class BasicData(Base):
    __tablename__ = f'{UNI_NAME}_basic_data'
    
    url = Column(Text, primary_key=True)
    parser = Column(Text)
    source = Column(Text)
    topic_block = Column(Text)
    parsing_date = Column(Date)
    public_date = Column(Date)
    title = Column(Text)
    context = Column(Text)
    raw_html = Column(Text)
    is_document = Column(Boolean)

class TimetableData(Base):
    __tablename__ = f'{UNI_NAME}_timetable_data'
    
    url = Column(Text, primary_key=True)
    parser = Column(Text)
    source = Column(Text)
    topic_block = Column(Text)
    parsing_date = Column(Date)
    public_date = Column(Date)
    title = Column(Text)
    context = Column(Text)
    raw_html = Column(Text)
    is_document = Column(Boolean)

class NewsData(Base):
    __tablename__ = f'{UNI_NAME}_news_data'
    
    url = Column(Text, primary_key=True)
    parser = Column(Text)
    source = Column(Text)
    topic_block = Column(Text)
    parsing_date = Column(Date)
    public_date = Column(Text)
    title = Column(Text)
    context = Column(Text)
    raw_html = Column(Text)
    is_document = Column(Boolean)

#Добавление таблиц в БД
# engine = create_engine(f"postgresql://..../{DB_NAME}")
# Base.metadata.create_all(engine)


