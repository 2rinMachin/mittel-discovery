from fastapi import APIRouter, HTTPException
from typing import List
from .services import *

router = APIRouter()

@router.get("/discover/articles/recent", response_model = List[Article])
async def discover_recent(limit: int = 10, skip: int = 0):
   return await get_recent_articles(limit, skip)

@router.get("/discover/articles/featured", response_model = List[Article])
async def discover_featured(limit: int = 10, skip: int = 0):
   return await get_featured_articles(limit, skip)

@router.get("/discover/articles/{post_id}", response_model = Article)
async def discover_article(post_id: str):
    article = await get_article_by_id(post_id)
    if not article: raise HTTPException(status_code = 404, detail = "Article not found")
    return article

@router.get("/discover/articles/tag/{tag}", response_model = List[Article])
async def discover_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    return await get_articles_by_tag(tag, limit, skip)

@router.get("/discover/articles/title/{title}", response_model = List[Article])
async def discover_articles_by_title(title: str, limit: int = 10, skip: int = 0):
    return await get_articles_by_title(title, limit, skip)

@router.get("/discover/comments/{post_id}", response_model = List[Comment])
async def discover_comments_for_post(post_id: str, limit: int = 10, skip: int = 0):
    return await get_comments_for_post(post_id, limit, skip)

@router.get("/discover/users/{user_id}", response_model = User)
async def discover_user_by_id(user_id: str):
    user = await get_user_by_id(user_id)
    if not user: raise HTTPException(status_code = 404, detail = "User not found")
    return user

@router.get("/discover/users/name/{user_username}", response_model = User)
async def discover_user_by_username(user_username: str):
    user = await get_user_by_username(user_username)
    if not user: raise HTTPException(status_code = 404, detail = "User not found")
    return user

@router.get("/")
async def hello_world():
    return { "message" : "And he wept, for there were no more backends to fix." }
