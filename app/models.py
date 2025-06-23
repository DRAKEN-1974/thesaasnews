from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    publication_date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    sentiment = Column(Float, nullable=True)

class ArticleStatistics(Base):
    __tablename__ = "article_statistics"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, unique=True, nullable=False)
    count = Column(Integer, nullable=False)