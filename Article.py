import newspaper
import time

class Article(object):

    def __init__(self, url):
        article = newspaper.build_article(url)
        article.download()
        article.parse()
        self.url = url
        self.text = article.text
        self.title = article.title
        self.download_date = time.localtime()

        # Optional parameters
        if article.authors:
            self.authors = article.authors
        else:
            self.authors = None

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
