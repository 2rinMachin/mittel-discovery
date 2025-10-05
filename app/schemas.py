import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class EngagementSummary(BaseModel):
    views: int = 0
    likes: int = 0
    shares: int = 0
    score: int = 0

class Author(BaseModel):
    id: str
    username: str
    email: str

class Article(BaseModel):
    id: str = Field(alias = "_id")
    title: str
    content: Optional[str] = None
    tags: List[str]
    author: Author
    commentsCount: int
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    engagement: Optional[EngagementSummary] = None

    class Config:
        extra = "ignore" # ignores all other fields
        populate_by_name = True # allows importing both _id and id!
        validate_by_name = True # allows exporting only id!

# WIP, not complete yet!
class User(BaseModel):
    id: str
    email: str
    username: Optional[str] = None

# note: author_id does not correspond with User.id
class Comment(BaseModel):
    id: str = Field(alias = "_id")
    postId: str
    content: str
    author: Author
    createdAt: Optional[str]
    updatedAt: Optional[str]


