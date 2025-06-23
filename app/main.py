from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from .database import Base, engine, SessionLocal
from .scraper import Scraper
from .processor import DataProcessor
from .api_integration import APIIntegration

import asyncio

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SaaS News Scraper API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    scraper = Scraper()
    processor = DataProcessor(scraper.base_url)
    api_integration = APIIntegration()
    articles_raw = await scraper.scrape_articles(max_pages=1)
    articles = processor.process_articles(articles_raw)
    db = SessionLocal()
    for art in articles:
        sentiment = api_integration.analyze_sentiment(art['headline'])
        db_article = models.Article(
            headline=art["headline"],
            url=art["url"],
            publication_date=art["publication_date"],
            category=art["category"],
            sentiment=sentiment
        )
        db.merge(db_article)
    db.commit()
    stats = processor.compute_statistics(articles)
    for stat in stats:
        db_stat = models.ArticleStatistics(
            category=stat["category"],
            count=stat["count"]
        )
        db.merge(db_stat)
    db.commit()
    db.close()

@app.get("/articles", response_model=List[schemas.ArticleOut])
def get_articles(category: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Article)
    if category:
        query = query.filter(models.Article.category == category)
    return query.all()

@app.get("/article/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.post("/articles", response_model=schemas.ArticleOut, status_code=201)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.get("/article-statistics", response_model=List[schemas.ArticleStatisticsOut])
def get_statistics(db: Session = Depends(get_db)):
    stats = db.query(models.ArticleStatistics).all()
    return stats