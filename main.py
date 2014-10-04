import crawlers

import sys
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('retina-crawler')

def main():
    logger.info('RETINA Crawler starting..')
    try:
        if len(sys.argv) != 2:
            print "Usage: python main.py path/to/config.json"
            sys.exit(1)
        
        config_file_path = sys.argv[1]
        with open(config_file_path) as f:
            config = json.load(f)
        crawler_type = getattr(crawlers, config['crawler'])
        logger.info('Loaded crawler "{}"'.format(config['crawler']))
        crawler = crawler_type(config['args'])
    except Exception, e:
        logger.exception("Invalid configuration: %s" % e)
        sys.exit(-1)

    try:
        logger.info("Running at %d" % int(time.time()))
        crawler.crawl()
    except Exception, e:
        logger.exception(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()
