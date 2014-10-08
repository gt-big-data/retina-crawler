import feedparser
from article import Article

class RssLinkParser(object):
    def __init__(self, rss_url):
        self.etag = None
        self.rss_url = rss_url

    def get_new_articles(self):
        feed = feedparser.parse(self.rss_url, etag = self.etag)
        if 'etag' in feed:
            self.etag = feed.etag
        articles = []
        for entry in feed.entries:
            articles.append(Article.create(entry.link))
        return articles
