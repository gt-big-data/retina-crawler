import newspaper
from datetime import datetime
import parsers
from urlparse import urlparse


parser_lookup = [
    ('cnn.com', parsers.parse_cnn_article),
]

def _getParserForUrl(url):
    for domain, parser in parser_lookup:
        if domain in url:
            return parser
    return None

class Article(object):

    def to_dict(self):
        # Return a copy of all public values.
        return {k: v for k, v in self.__dict__.iteritems() if not k.startswith('_')}

    def __init__(self, url, parser=None):
        self.url = url
        self.source_domain = None
        self.text = None
        self.title = None
        self.download_date = None
        self.authors = None
        self.categories = None
        self.keywords = None
        self.images = None
        self.location = None
        self.summary = None
        self.suggested_articles = None
        self.meta_favicon = None
        self.meta_lang = None
        self.pub_date = None
        self.html = None
        self._parsed = False
        self._parser = parser or _getParserForUrl(url)

    def download_and_parse(self):
        if self._parsed:
            raise Exception('This article ({}) has already been parsed.'.format(self.url))

        article = newspaper.build_article(self.url)
        article.download()
        article.parse()
        self.text = article.text
        self.title = article.title
        self.html = article.html
        self.download_date = datetime.now()

        # Optional parameters
        if article.authors:
            self.authors = article.authors
        else:
            self.authors = None

        self.source_domain = urlparse(self.url).netloc

        # Not sure how to implement right now
        self.category = None

        # Merge keywords and meta_keywords into the same param
        self.keywords = []
        if article.keywords:
            self.keywords = article.keywords
        if article.meta_keywords:
            self.keywords = list(set(self.keywords + article.meta_keywords))

        if self.keywords == ['']:
            self.keywords = None

        if article.images:
            self.images = article.images
        else:
            self.images = None

        # Will implement later
        self.location = None

        if article.summary:
            self.summary = article.summary
        else:
            self.summary = None

        # Not sure how to implement
        self.suggested_articles = None

        if article.meta_favicon:
            self.meta_favicon = article.meta_favicon
        else:
            self.meta_favicon = None

        if article.meta_lang:
            self.meta_lang = article.meta_lang
        else:
            self.meta_lang = None

        if article.published_date:
            self.pub_date = article.published_date
        else:
            self.pub_date = None

        if self._parser:
            self._parser(self)

        self._parsed = True

class RssArticle(Article):

    def __init__(self, link, published_date, title, summary, parser=None):
        super(RssArticle, self).__init__(link, parser)
        self._rss_published_date = published_date
        self._rss_title = title
        self._rss_summary = summary

    def download_and_parse(self):
        super(RssArticle, self).download_and_parse()
        self.title = self._rss_title or self.title
        self.summary = self._rss_summary or self.summary
        self.pub_date = self._rss_published_date or self.pub_date
