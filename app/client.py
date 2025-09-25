import os
from dotenv import load_dotenv
import httpx

load_dotenv()
BASE_URL_AUTH = os.getenv("BASE_URL_AUTH")
BASE_URL_ARTICLES = os.getenv("BASE_URL_ARTICLES")
BASE_URL_ENGAGEMENT = os.getenv("BASE_URL_ENGAGEMENT")

async def fetch_one_article(article_id: str):
    async with httpx.AsyncClient() as client:
        try: 
            resp = await client.get(f"{BASE_URL_ARTICLES}/articles/{article_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: return None
        

async def fetch_recent_articles(limit: int = 10, skip: int = 0):
    async with httpx.AsyncClient() as client:
        params = { "limit" : limit, "skip" : skip }
        resp = await client.get(f"{BASE_URL_ARTICLES}/articles/recent", params = params)
        resp.raise_for_status()
        return resp.json()

async def fetch_engagement(post_id: str):
    async with httpx.AsyncClient() as client:
        params = { "post_id" : post_id }
        try: 
            resp = await client.get(f"{BASE_URL_ENGAGEMENT}/events/summary", params = params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: return { "views" : 0, "likes" : 0, "shares" : 0 }

async def fetch_user(user_id: str):
    async with httpx.AsyncClient() as client:
        try: 
            resp = await client.get(f"{BASE_URL_AUTH}/users/{user_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: return None

async def fetch_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    async with httpx.AsyncClient() as client:
        params = { "limit" : limit, "skip" : skip }
        resp = await client.get(f"{BASE_URL_ARTICLES}/articles/tag/{tag}", params = params)
        resp.raise_for_status()
        return resp.json()
