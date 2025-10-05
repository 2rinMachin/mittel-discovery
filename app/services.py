from . import client
from .schemas import *

async def get_article_engagement(article: Article):
    engagement_data = await client.fetch_engagement(article.id)
    summary = EngagementSummary.model_validate(engagement_data)
    summary.score = 5*summary.shares + 2*summary.likes + summary.views
    article.engagement = summary
    return article

async def get_recent_articles(limit: int = 10, skip: int = 0):
    feed_articles_data = await client.fetch_recent_articles(limit, skip);
    if not feed_articles_data: return []
    ids = []
    raw_data = []
    res_articles = []
    for feed_article in feed_articles_data: ids.append(feed_article["_id"])
    for id in ids: raw_data.append(await get_article_by_id(id))
    for raw in raw_data: res_articles.append(await get_article_engagement(Article.model_validate(raw)))
    return res_articles


async def get_featured_articles(limit: int = 10, skip: int = 0):
    res_articles = await get_recent_articles(limit, skip)
    res_articles.sort(key = lambda article: article.engagement.score if article.engagement else 0, reverse = True)
    return res_articles

async def get_article_by_id(article_id: str):
    article_data = await client.fetch_one_article(article_id)
    if not article_data: return None
    article = Article.model_validate(article_data)
    return await get_article_engagement(article)

async def get_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    articles_data = await client.fetch_articles_by_tag(tag, limit, skip)
    if not articles_data: return []
    res_articles = []
    for article in articles_data:
        res_articles.append(await get_article_engagement(Article.model_validate(article)))
    res_articles.sort(key = lambda article: article.engagement.score if article.engagement else 0, reverse = True)
    return res_articles

async def get_articles_by_title(title: str, limit: int = 10, skip: int = 0):
    articles_data = await client.fetch_articles_by_title(title, limit, skip)
    if not articles_data: return []
    res_articles = []
    for article in articles_data:
        res_articles.append(await get_article_engagement(Article.model_validate(article)))
    res_articles.sort(key = lambda article: article.engagement.score if article.engagement else 0, reverse = True)
    return res_articles

async def get_comments_for_post(post_id: str, limit: int = 10, skip: int = 0):
    comments_data = await client.fetch_comments_by_post(post_id, limit, skip)
    res_comments = []
    for comment in comments_data: res_comments.append(Comment.model_validate(comment))
    return res_comments

async def get_user_by_id(user_id: str):
    user_data = await client.fetch_user_by_id(user_id)
    if not user_data: return None
    return User.model_validate(user_data)

async def get_user_by_username(user_username: str):
    user_data = await client.fetch_user_by_username(user_username)
    if not user_data: return None
    return User.model_validate(user_data)
