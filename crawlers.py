from RssFeedParser import RssLinkParser
from writers import *
from article import Article
from downloaders import *
import multiprocessing
import sys

class ModularCrawler(object):
    def _get_writer(self, args):
        """Create and return an output writer based on the given input value.

        Arguments:
        args -- The args variable given to the crawler.

        Return the appropriate writer requested. Will raise an exception if something goes wrong.
        """
        try:
            output = args["output"].lower()
        except KeyError:
            raise ValueError("Must specify an output type.")
        except AttributeError:
            raise ValueError("'output' must be a string.")

        if output == "file":
            return FileWriter()
        elif output == "mongo":
            try:
                mongo_kw_args = args['mongo_params']
            except KeyError:
                raise ValueError("'mongo_params' must be specified when writing to MongoDB.")
            try:
                return MongoWriter(**mongo_kw_args)
            except TypeError:
                raise ValueError("'mongo_params' requires a host and port. The following was given: %s" % mongo_kw_args)
        elif output == "print":
            return PrintWriter()
        else:
            raise ValueError("Could not interpret the given output type: %s" % output)

    def _get_threads(self, args):
        """Determine the number of threads/processes the crawler should work with.

        Arguments:
        args -- The args variable given to the crawler.

        Return an integer representing the number of processes to spawn for this crawler. Will 
        raise an exception if something goes wrong.
        """
        try:
            threads = int(args["threads"])
        except KeyError:
            raise ValueError("Must specify the number of threads the crawler should work with.")
        except ValueError:
            raise ValueError("Threads must be an integer.")
        if threads < 0:
            raise ValueError("Threads must be a positive integer.")
        # 0 is interpreted as make as many threads as there are cores.
        if threads == 0:
            threads = multiprocessing.cpu_count()
        return threads

    def _get_downloader(self, writer, threads):
        """Create and return a Downloader for downloading articles with.

        Arguments:
        writer -- The output writer to use.
        threads -- The number of threads to utilize.
        
        Return a Downloader for downloading articles.
        """
        if threads == 1:
            return SingleThreadedDownloader(writer)
        else:
            return MultiProcessDownloader(threads, writer)

    def __init__(self, args):
        writer = self._get_writer(args)
        threads = self._get_threads(args)
        downloader = self._get_downloader(writer, threads)
        
        try:
            urls = args["urls"]
        except KeyError:
            # Passing in individual URLs is optional.
            pass
        else:
            try:
                for url in urls:
                    article = Article(url)
                    downloader.queue_article(article)
            except TypeError:
                raise ValueError("'urls' must be a list of article URLs to process.")

        try:
            feeds = args["feeds"]
        except KeyError:
            # Passing in feeds is optional.
            pass
        else:
            try:
                for feed in feeds:
                    feed_parser = RssLinkParser(feed)
                    for article in feed_parser.get_new_articles():
                        downloader.queue_article(article)
            except TypeError:
                raise ValueError("'feeds' must be a list of RSS feed URLs to process.")

        self._downloader = downloader

    def crawl(self):
        # process_all(), by design, is not supposed to throw any errors.
        self._downloader.process_all()
