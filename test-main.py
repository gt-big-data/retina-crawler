from article import Article
import json
import unittest
from datetime import datetime
from urllib.parse import urlparse
from os import path
from main import load_config

class BaseSiteTest(unittest.TestCase):
    def __init__(self, json_file):
        super(self.__class__, self).__init__()
        self.json_file = json_file
        self.article = None

    def runTest(self):
        for test in dir(self):
            if test.startswith("test"):
                getattr(self, test)()

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
        with open(self.json_file) as json_data:
            self.data = json.load(json_data)

        self._parse()

    def all_tests(self):
        pass

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
        self.assertEqual(self.data["recent_pub_date"], self.article.pub_date)

if __name__ == '__main__':
    config = load_config(path.join("configs", "test-file-generator.json"))
    data = [filename for filename, url in config["args"]["known_good_urls"]]
    print("Working...")
    suites = []
    for d in data:
        json_file = path.join("test_files", d)
        print("Loading: %s" % json_file)
        test_suite = BaseSiteTest(json_file)
        suites.append(test_suite)

    runner = unittest.TextTestRunner()
    for suite in suites:
        runner.run(suite)
