import json
from bs4 import BeautifulSoup
from fastapi.params import Depends
import requests
from sqlalchemy.orm.session import Session
from fastapi import FastAPI, HTTPException, status
from sqlalchemy import engine
from starlette.status import HTTP_404_NOT_FOUND
from . import models
from .database import SessionLocal, engine
from .models import RssResults

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get('/rss', tags=['RSS'])
def financialreporter_rss(db: Session = Depends(get_db)):
    article_list = []

    try:
        r = requests.get('https://www.financialreporter.co.uk/rss.asp?v=1')
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            article = RssResults(title=title, link=link, published=published)
            article_list.append(article)
        db.add_all(article_list)
        db.commit()
        return {'message': 'Added Successfully'}
        
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


@app.get('/search/{text}', tags=['RSS'])
def search_title(text: str, db: Session = Depends(get_db)):
    results = db.query(models.RssResults).filter(RssResults.title.ilike(f'%{text}%')).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Title with the word '{text}' is not available")
    return results