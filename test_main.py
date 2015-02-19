from article import Article
import json
import unittest
from datetime import datetime
from urlparse import urlparse

class TestParser(unittest.TestCase):
    # Don't test article.download_date because I'm faking it anyways.
    def _parse(self):
        article = Article(self.data["url"])
        # Fake article.download()
        article.download_date = datetime.utcnow()
        article.source_domain = urlparse(article.url).netloc
        article.html = self.data["html"]

        article.parse()
        self.article = article

    def setUp(self):
        # self.data is a dict that vaguely resembles what a fully constructed
        # Article would look like.
        with open("test_files/basic.json") as data:
            self.data = json.load(data)
        self.data["download_date"] = datetime.utcnow()
        with open("test_files/basic.html") as html:
            self.data["html"] = html.read()
        self.article = None

        self._parse()

    def test_url(self):
        self.assertEqual(self.data["url"], self.article.url)

    def test_source_domain(self):
        self.assertEqual(self.data["source_domain"], self.article.source_domain)

    def test_text(self):
        self.assertEqual(self.data["text"], self.article.text)

    def test_title(self):
        self.assertEqual(self.data["title"], self.article.title)

    def test_summary(self):
        self.assertEqual(self.data["summary"], self.article.summary)

    def test_authors(self):
        self.assertEqual(self.data["authors"], self.article.authors)

    def test_categories(self):
        self.assertEqual(self.data["categories"], self.article.categories)

    def test_keywords(self):
        self.assertEqual(self.data["keywords"], self.article.keywords)

    def test_images(self):
        self.assertEqual(self.data["images"], self.article.images)

    def test_suggested_articles(self):
        self.assertEqual(self.data["suggested_articles"], self.article.suggested_articles)

    def test_meta_favicon(self):
        self.assertEqual(self.data["meta_favicon"], self.article.meta_favicon)

    def test_location(self):
        self.assertEqual(self.data["location"], self.article.location)

    def test_download_date(self):
        # We are faking the download date so I'd rather not test for it.
        pass

    def test_meta_lang(self):
        # Not grabbing meta_lang yet.
        pass
        #self.assertEqual(self.data["meta_lang"], self.article.meta_lang)

    def test_pub_date(self):
        self.assertEqual(self.data["pub_date"], self.article.pub_date)

if __name__ == '__main__':
    unittest.main()
