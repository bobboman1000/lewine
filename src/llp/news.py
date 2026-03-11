import feedparser
from newspaper import Article
from dataclasses import dataclass


@dataclass
class News:
    title: str
    text: str
    link: str

    def get(self, attr, default=None):
        if attr in self.__dict__:
            return attr.__getattribute__(attr)
        else:
            return default

def get_news(rss_urls: list[str], limit_articles: int = 2) -> list[News]:

    # fetch news info
    feeds = [_get_news_info(rss_url) for rss_url in rss_urls]
    news_infos = [news_entry for feed in feeds for news_entry in feed]
    news_items = []

    if len(news_infos) > limit_articles:
        news_infos = news_infos[:limit_articles]

    # enrich news info with actual full text obtained from the link
    for item in news_infos:
        article = _extract_article(item['link'])
        news_items.append(
            News(
                article['title'],
                article['text'],
                item['link']
            )
        )
    return news_items

def _get_news_info(rss_url: str, max_items: int = 10) -> list[dict]:
    feed = feedparser.parse(rss_url)
    news_items = []
    for entry in feed.entries[:max_items]:
        news_items.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'summary': entry.get('summary', '')
        })
    return news_items


def _extract_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return {
        'title': article.title,
        'text': article.text
    }