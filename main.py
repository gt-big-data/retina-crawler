from RssFeedParser import RssLinkParser
from downloaders import *
from writers import *

import crawlers
import sys
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('retina-crawler')

def find_articles(url):
    feed_parser = RssLinkParser(url)
    links = feed_parser.get_links()
    return links

def main():
    logger.info('RETINA CRAWLER starting..')
    try:
        if len(sys.argv) < 2:
            crawler = crawlers.SimpleCrawler()
        else:
            config_file_path = sys.argv[1]
            with open(config_file_path) as f:
                config = json.load(f)
            crawler_type = getattr(crawlers, config['crawler'])
            logger.info('loaded crawler "{}"'.format(config['crawler']))
            crawler = crawler_type(config['args'])
    except Exception, e:
        logger.exception('Invalid config given, error is "{}"'.format(e))
        sys.exit(-1)

    try:
        logger.info('Running at {}'.format(time.time()))
        crawler.crawl()
    except Exception, e:
        logger.exception(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()
