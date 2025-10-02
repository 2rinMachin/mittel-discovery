from . import client
from .schemas import Article, EngagementSummary, User

async def get_article_engagement(article: Article):
    engagement_data = await client.fetch_engagement(article.post_id)
    if not engagement_data: engagement_data = { "views": 0, "likes": 0, "shares": 0 }
    summary = EngagementSummary(**engagement_data)
    summary.score = 5*summary.shares + 2*summary.likes + summary.views
    article.engagement = summary
    return article

async def get_article_by_id(article_id: str):
    article_data = await client.fetch_one_article(article_id)
    if not article_data: return None
    article = Article(**article_data)
    return await get_article_engagement(article)

async def get_recent_articles(limit: int = 10, skip: int = 0):
    articles_data = await client.fetch_recent_articles(limit, skip)
    if not articles_data: return []
    res_articles = []
    for article in articles_data: res_articles.append(await get_article_engagement(Article(**article)))
    return res_articles

async def get_user_by_id(user_id: str):
    user_data = await client.fetch_user(user_id)
    if not user_data: return None
    return User(**user_data)

async def get_articles_by_tag(tag: str, limit: int = 10, skip: int = 0):
    articles_data = await client.fetch_articles_by_tag(tag, limit, skip)
    if not articles_data: return []
    res_articles = []
    for article in articles_data: res_articles.append(await get_article_engagement(Article(**article)))
    return res_articles

async def get_articles_by_title(title: str, limit: int = 10, skip: int = 0):
    if not title.strip(): return []
    articles_data = await client.fetch_recent_articles(limit, skip)
    if not articles_data: return []
    res_articles = []
    for article in articles_data:
        if title.lower() in article["title"].lower():
            res_articles.append(await get_article_engagement(Article(**article)))
        if len(res_articles) >= limit: break
    res_articles.sort(key = lambda article: article.engagement.score if article.engagement else 0, reverse = True)
    return res_articles
