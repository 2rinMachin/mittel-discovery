from . import client
from .schemas import *
import asyncio

_semaphore = asyncio.Semaphore(10)

async def get_article_engagement(article: Article):
    async with _semaphore:
        engagement_data = await client.fetch_engagement(article.id)
    summary = EngagementSummary.model_validate(engagement_data)
    summary.score = 5*summary.shares + 2*summary.likes + summary.views
    article.engagement = summary
    return article

async def get_article_by_id(article_id: str):
    async with _semaphore:
        article_data = await client.fetch_one_article(article_id)
    if not article_data: return None
    article = Article.model_validate(article_data)
    return await get_article_engagement(article)

async def get_recent_articles(limit: int = 10, skip: int = 0):
    async with _semaphore:
        feed_articles_data = await client.fetch_recent_articles(limit, skip)
    if not feed_articles_data: return []
    ids = [feed_article["_id"] for feed_article in feed_articles_data]
    raw_articles = await asyncio.gather(*(get_article_by_id(id) for id in ids))
    return [a for a in raw_articles if a is not None]

async def get_featured_articles(limit: int = 10, skip: int = 0):
    res_articles = await get_recent_articles(limit, skip)
    res_articles.sort(key=lambda article: article.engagement.score if article.engagement else 0, reverse=True)
    return res_articles

async def get_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    async with _semaphore: articles_data = await client.fetch_articles_by_tag(tag, limit, skip)
    if not articles_data: return []
    ids = [article["_id"] for article in articles_data]
    full_articles = await asyncio.gather(*(get_article_by_id(id) for id in ids))
    full_articles = [a for a in full_articles if a is not None]
    full_articles.sort(key=lambda article: article.engagement.score if article.engagement else 0, reverse=True)
    return full_articles

async def get_articles_by_title(title: str, limit: int = 10, skip: int = 0):
    async with _semaphore: articles_data = await client.fetch_articles_by_title(title, limit, skip)
    if not articles_data: return []
    ids = [article["_id"] for article in articles_data]
    full_articles = await asyncio.gather(*(get_article_by_id(id) for id in ids))
    full_articles = [a for a in full_articles if a is not None]
    full_articles.sort(key=lambda article: article.engagement.score if article.engagement else 0, reverse=True)
    return full_articles


async def get_comments_for_post(post_id: str, limit: int = 10, skip: int = 0):
    async with _semaphore:
        comments_data = await client.fetch_comments_by_post(post_id, limit, skip)
    return [Comment.model_validate(c) for c in comments_data]

async def get_user_by_id(user_id: str):
    async with _semaphore:
        user_data = await client.fetch_user_by_id(user_id)
    if not user_data: return None
    return Author.model_validate(user_data)

async def get_user_by_username(user_username: str):
    async with _semaphore:
        user_data = await client.fetch_user_by_username(user_username)
    if not user_data: return None
    return Author.model_validate(user_data)

async def get_articles_by_author(author_id: str, limit: int = 10, skip: int = 0):
    async with _semaphore:
        article_data = await client.fetch_articles_by_author(author_id, limit, skip)
    if not article_data: return []
    res_articles = await asyncio.gather(*(get_article_engagement(Article.model_validate(article)) for article in article_data))
    return [a for a in res_articles if a is not None]

async def get_author_score(user_id: str):
    articles_data, user_data = await asyncio.gather(get_articles_by_author(user_id), get_user_by_id(user_id))
    if not user_data or not articles_data: return None
    score = sum(article.engagement.score for article in articles_data if article.engagement)
    return AuthorScore.model_validate({"id": user_id, "username": user_data.username, "score": score})

async def get_ranked_authors(limit: int = 10, skip: int = 0):
    recent_data = await get_recent_articles(limit, skip)
    if not recent_data: return None
    author_ids = list({article.author.id for article in recent_data if article.author})
    author_scores = await asyncio.gather(*(get_author_score(id) for id in author_ids))
    author_scores = [a for a in author_scores if a is not None]
    author_scores.sort(key=lambda a: a.score, reverse=True)
    return author_scores

