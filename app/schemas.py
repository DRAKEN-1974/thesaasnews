from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    headline: str
    url: str
    publication_date: datetime
    category: str
    sentiment: Optional[float] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleOut(ArticleBase):
    id: int
    class Config:
        orm_mode = True

class ArticleStatisticsOut(BaseModel):
    category: str
    count: int