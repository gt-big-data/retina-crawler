import requests
from datetime import datetime
import parsers
from urllib.parse import urlparse
from lxml.html.clean import clean_html
from lxml.html import document_fromstring

class Article(object):

    def to_dict(self):
        # Return a copy of all public values.
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __init__(self, url, parser=None):
        self.url = url
        self.source_domain = None
        self.text = None
        self.title = None
        self.depth = None
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
        self.out_links = []

    def parse(self):
        # This alters the html in-place.
        clean_html(self.html)
        doc = document_fromstring(self.html)
        parsers.parse_article(self, doc)
        self._parsed = True

    def download(self):
        self.download_date = datetime.utcnow()
        self.source_domain = urlparse(self.url).netloc
        try:
            response = requests.get(self.url)
            self.html = response.content.decode()
            self.url = response.url # Deals with redirects.
        except requests.exceptions.RequestException:
            raise IOError("Could not download the article at: %s" % self.url)

    def download_and_parse(self):
        if self._parsed:
            raise Exception('This article ({}) has already been parsed.'.format(self.url))
        self.download()
        self.parse()

class RecursiveArticle(Article):
    def __init__(self, link, link_sink, depth=0, parent_url=None):
        super(RecursiveArticle, self).__init__(link)
        self._link_sink = link_sink
        self.depth = depth
        self.parent_url = parent_url

    def download_and_parse(self):
        super(RecursiveArticle, self).download_and_parse()
        for out_link in self.out_links:
            self._link_sink.add_article_url(self, out_link)
