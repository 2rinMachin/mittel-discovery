import os
from dotenv import load_dotenv
import httpx

load_dotenv()
BASE_URL_AUTH = os.getenv("BASE_URL_AUTH")
BASE_URL_ARTICLES = os.getenv("BASE_URL_ARTICLES")
BASE_URL_ENGAGEMENT = os.getenv("BASE_URL_ENGAGEMENT")

async def fetch_engagement(post_id: str | None = None, user_id: str | None = None):
    async with httpx.AsyncClient() as client:
        params = { }
        if post_id: params["post_id"] = post_id
        if user_id: params["user_id"] = user_id
        try: 
            resp = await client.get(f"{BASE_URL_ENGAGEMENT}/events", params = params, headers={"X-Internal-Token": "123456"})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: return None
            elif e.response.status_code == 401: raise Exception("Unauthorized when fetching engagement")
            raise

# fetch to /articles/recent always is 200 OK
# handled as [] in mittel-articles
async def fetch_recent_articles(limit: int = 10, skip: int = 0):
    async with httpx.AsyncClient() as client:
        params = { "limit" : limit, "skip" : skip }
        resp = await client.get(f"{BASE_URL_ARTICLES}/articles/search", params = params)
        resp.raise_for_status()
        return resp.json()

async def fetch_one_article(article_id: str):
    async with httpx.AsyncClient() as client:
        try: 
            resp = await client.get(f"{BASE_URL_ARTICLES}/articles/{article_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: return None
            raise

# fetch to /articles/search always is 200 OK
# handled as [] in mittel-articles
async def fetch_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    async with httpx.AsyncClient() as client:
        params = { "tag" : tag, "limit" : limit, "skip" : skip }
        resp = await client.get(f"{BASE_URL_ARTICLES}/articles/search", params = params)
        resp.raise_for_status()
        return resp.json()

# fetch to /articles/search always is 200 OK
# handled as [] in mittel-articles
async def fetch_articles_by_title(title: str, limit: int = 10, skip: int = 0):
    async with httpx.AsyncClient() as client:
        params = { "title" : title, "limit" : limit, "skip" : skip }
        resp = await client.get(f"{BASE_URL_ARTICLES}/articles/search", params = params)
        resp.raise_for_status()
        return resp.json()

async def fetch_comments_by_post(post_id: str, limit: int = 10, skip: int = 0):
    async with httpx.AsyncClient() as client:
        params = { "limit" : limit, "skip" : skip }
        resp = await client.get(f"{BASE_URL_ARTICLES}/comments/post/{post_id}", params = params)
        resp.raise_for_status()
        return resp.json()

# WIP
async def fetch_user(user_id: str):
    async with httpx.AsyncClient() as client:
        try: 
            resp = await client.get(f"{BASE_URL_AUTH}/users/{user_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404: return None
            raise

