from sqlalchemy import Column, Integer, String
from .database import Base


class RssResults(Base):
    __tablename__ = 'rssresults'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    link = Column(String)
    published = Column(String)