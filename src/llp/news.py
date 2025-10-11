import feedparser
from newspaper import Article

def fetch_news(rss_url: str, max_items: int =10):
    """
    Fetches news items from the given RSS feed URL.

    Args:
        rss_url (str): The URL of the RSS feed.
        max_items (int): Maximum number of news items to return.

    Returns:
        list[dict]: List of news items with 'title', 'link', and 'summary'.
    """
    feed = feedparser.parse(rss_url)
    news_items = []
    for entry in feed.entries[:max_items]:
        news_items.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'summary': entry.get('summary', '')
        })
    return news_items


def extract_article(url):
    """
    Extracts the main news article from the given URL.

    Args:
        url (str): The URL of the news article.

    Returns:
        dict: Dictionary with 'title' and 'text' of the article.
    """
    article = Article(url)
    article.download()
    article.parse()
    return {
        'title': article.title,
        'text': article.text
    }