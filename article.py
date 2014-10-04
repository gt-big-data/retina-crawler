import newspaper
import time

class Article(object):

    def __init__(self, url, parser=None):
        self.url = url
        self.source_domain = None
        self.text = None
        self.title = None
        self.download_date = None
        self.authors = None
        self.category = None
        self.keywords = None
        self.images = None
        self.location = None
        self.summary = None
        self.suggested_articles = None
        self.meta_favicon = None
        self.meta_lang = None
        self.pub_date = None
        self.html = None
        self.parsed = False
        self._parser = parser

    def download_and_parse(self):
        article = newspaper.build_article(self.url)
        article.download()
        article.parse()
        self.text = article.text
        self.title = article.title
        self.html = article.html
        self.download_date = int(time.time())

        # Optional parameters
        if article.authors:
            self.authors = article.authors
        else:
            self.authors = None

        self.source_domain = None

        # Not sure how to implement right now
        self.category = None

        # Merge keywords and meta_keywords into the same param
        self.keywords = []
        if article.keywords:
            self.keywords = article.keywords
        if article.meta_keywords:
            self.keywords = list(set(self.keywords + article.meta_keywords))

        if self.keywords == ['']:
            keywords = None

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

        self.parsed = True
