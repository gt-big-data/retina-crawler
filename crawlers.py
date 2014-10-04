from RssFeedParser import RssLinkParser
from writers import *
import article
from downloaders import *
import multiprocessing
import sys

class ModularCrawler(object):
    def __init__(self, args):
        try:
            output = args["output"].lower()
            if output == "file":
                writer = FileWriter()
            elif output == "mongo":
                mongo_kw_args = args['mongo_params']
                writer = MongoWriter(**mongo_kw_args)
            elif output == "print":
                writer = PrintWriter()
            else:
                # Make this more specific
                raise Exception
        except Exception, e:
            raise e
            sys.exit(-1)

        try:
            threads = int(args["threads"])
            if threads == 0:
                threads = multiprocessing.cpu_count()
        except Exception, e:
            #TODO: Add logging about bad args because threads was weird.
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
            urls = args["urls"]
            for url in urls:
                downloader.queue_link(url)
        except Exception, e:
            #TODO: Add logging about bad config because no threads given.
            sys.exit(-1)

        try:
            feeds = args["feeds"]
            for feed in feeds:
                feed_parser = RssLinkParser(feed)
                for link in feed_parser.get_new_links():
                    downloader.queue_link(link)
        except Exception, e:
            print e
            raise
            #TODO: Add logging code.
            sys.exit(-1)

        self._downloader = downloader

    def crawl(self):
        # process_all(), by design, is not supposed to throw any errors.
        self._downloader.process_all()
