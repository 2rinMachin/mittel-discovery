from pydantic import BaseModel
from typing import Optional

class EngagementSummary(BaseModel):
    views: int
    likes: int
    shares: int
    score: Optional[int] = None

class Article(BaseModel):
    post_id: str
    title: str
    content: Optional[str] = None
    author_id: str
    engagement: Optional[EngagementSummary] = None

class User(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
