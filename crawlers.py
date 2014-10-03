from RssFeedParser import RssLinkParser, MultiRSSLinkParsers
from writers import *
import article
from downloaders import *
import multiprocessing
import sys

class ModularCrawler(object):
    def __init__(self, config):
        try:
            output = config["output"].lower()
            if output == "file":
                writer = FileWriter()
            elif output == "mongo":
                writer = MongoWriter()
            elif output == "print":
                writer = PrintWriter()
            else:
                # Make this more specific
                raise Exception
        except Exception, e:
            #TODO: Add logging about bad config because bad writer type.
            sys.exit(-1)

        try:
            threads = int(config["threads"])
            if threads == 0:
                threads = multiprocessing.cpu_count()
        except Exception, e:
            #TODO: Add logging about bad config because threads was weird.
            sys.exit(-1)

        try:
            if threads == 1:
                downloader = SingleThreadedDownloader(writer)
            else:
                downloader = MultiProcessDownloader(threads, writer)
        except Exception, e:
            # Log an error
            sys.exit(-1)

        try:
            urls = config["urls"]
            for url in urls:
                downloader.queue_link(url)
        except Exception, e:
            #TODO: Add logging about bad config because no threads given.
            sys.exit(-1)

        # TODO: Add support for grabbing feeds.

        self._downloader = downloader

    def crawl(self):
        # process_all(), by design, is not supposed to throw any errors.
        self._downloader.process_all()

class SeveralRSSMongoCrawler(object):
    def __init__(self, config):
        self._rssParser = MultiRSSLinkParsers(config['feeds'])
        mongo_kw_args = config['mongo_params'] if 'mongo_params' in config else {}

        self._article_writer = MongoWriter(**mongo_kw_args)

    def crawl(self):
        for link in self._rssParser.get_new_links():
            article_info = article.create_article(link)
            article_data = article.article_dictionary(article_info)
            self._article_writer.write(article_data)

class SimpleCrawler(object):
    def __init__(self):
        self._rssParser = RssLinkParser('http://rss.cnn.com/rss/edition.rss')

    def crawl(self):
        downloader = SingleThreadedDownloader(FileWriter())
        for article in self._rssParser.get_new_articles():
            downloader.queue_link(link)
        downloader.process_all()
