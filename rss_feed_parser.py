import feedparser
import urlparse
from article import RssArticle, Article
from time import mktime
from datetime import datetime

class RssFeedParser(object):
    def __init__(self, rss_url):
        self.etag = None
        self.rss_url = rss_url
        self.etag_filename = self._get_filename(rss_url)
        try:
            with open(self.etag_filename) as old_etag_file:
                etag = old_etag_file.read()
                if etag:
                    self.etag = etag
        except:
            pass

    def _get_filename(self, rss_url):
        p = urlparse.urlparse(rss_url)
        path_parts = [part for part in p.path.split('/') if part]
        path_formatted = '-'.join(path_parts)
        return '{domain}.{path}.etag'.format(
            domain=p.netloc,
            path=path_formatted
        )

    def get_new_articles(self):
        feed = feedparser.parse(self.rss_url, etag = self.etag)
        if 'etag' in feed:
            if feed.etag != self.etag:
                with open(self.etag_filename, 'w+') as etag_file:
                    etag_file.write(feed.etag)
            self.etag = feed.etag
        articles = []
        for entry in feed.entries:
            articles.append(
                RssArticle(
                    entry.link,
                    datetime.fromtimestamp(mktime(entry.published_parsed)),
                    entry.title,
                    entry.summary
                )
            )
        return articles

class MultipleRSSFeedParser(object):
    def __init__(self, feeds):
        self._parsers = [RssFeedParser(feed) for feed in feeds]

    def get_new_articles(self):
        new_articles = []
        for parser in self._parsers:
            new_articles.extend(parser.get_new_articles())
        return new_articles