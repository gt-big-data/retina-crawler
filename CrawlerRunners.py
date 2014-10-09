from RssFeedParser import RssLinkParser, MultiRSSLinkParsers
from writers import FileWriter, MongoWriter
import article

class SeveralRSSMongoRunner(object):
    def __init__(self, config):
        self._rssParser = MultiRSSLinkParsers(config['feeds'])
        mongo_kw_args = config['mongo_params'] if 'mongo_params' in config else {}
        
        self._article_writer = MongoWriter(**mongo_kw_args)

    def run(self):
        for link in self._rssParser.get_new_links():
            article_info = article.create_article(link)
            article_data = article.article_dictionary(article_info)
            self._article_writer.write(article_data)

class SimpleRunner(object):
    def __init__(self):
        self._rssParser = RssLinkParser('http://rss.cnn.com/rss/edition.rss')
        self._article_writer = FileWriter()

    def run(self):
        for link in self._rssParser.get_new_links():
            article_info = article.create_article(link)
            article_data = article.article_dictionary(article_info)
            self._article_writer.write(article_data)