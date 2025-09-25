from . import client
from .schemas import Article, EngagementSummary, User

async def get_article_engagement(article: Article):
    engagement_data = await client.fetch_engagement(article.post_id)
    if engagement_data: article.engagement = EngagementSummary(**engagement_data)
    return article

async def get_article_by_id(article_id: str):
    article_data = await client.fetch_one_article(article_id)
    if not article_data: return None
    article = Article(**article_data)
    return await get_article_engagement(article)

async def get_recent_articles(limit: int = 10, skip: int = 0):
    articles_data = await client.fetch_recent_articles(limit, skip)
    res_articles = []
    for article in articles_data: res_articles.append(await get_article_engagement(Article(**article)))
    return res_articles

async def get_user_by_id(user_id: str):
    user_data = await client.fetch_user(user_id)
    if not user_data: return None
    return User(**user_data)

async def get_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    articles_data = await client.fetch_articles_by_tag(tag, limit, skip)
    res_articles = []
    for article in articles_data: res_articles.append(await get_article_engagement(Article(**article)))
    return res_articles
