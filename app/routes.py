from fastapi import APIRouter, HTTPException
from typing import List
from .services import *

router = APIRouter(prefix = "/discover")

@router.get("/articles/{post_id}", response_model = Article)
async def discover_article(post_id: str):
    article = await get_article_by_id(post_id)
    if not article: raise HTTPException(status_code = 404, detail = "Article not found")
    return article

@router.get("/users/{user_id}", response_model = User)
async def discover_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user: raise HTTPException(status_code = 404, detail = "User not found")
    return user

@router.get("/articles/recent", response_model = List[Article])
async def discover_recent(limit: int = 10, skip: int = 0):
    return await get_recent_articles(limit, skip)

@router.get("/articles/tag/{tag}", response_model = List[Article])
async def discover_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    return await get_articles_by_tag(tag, limit, skip)
