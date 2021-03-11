from bs4.element import SoupStrainer
from fastapi.params import Depends
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm.session import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./RSS.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False)
Session.configure(bind=engine)
session = Session()

Base = declarative_base()

class RssResults(Base):
    __tablename__ = 'rssresults'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    link = Column(String)
    published = Column(String)


def get_arcticles():
    para_list = []
    article_links = session.query(RssResults.link).all()
    for article_link in article_links:
        print(article_link)
        page = requests.get(article_link[0])
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('article', class_='wrap-column-1')
        paras= results.find_all('p')
        for para in paras:
            para_list.append(para.get_text())

    print(para_list)
get_arcticles()
