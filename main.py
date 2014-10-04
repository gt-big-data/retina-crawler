import crawlers

import sys
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('retina-crawler')

def load_config(config_file_path):
    try:
        with open(config_file_path) as f:
            try:
                config = json.load(f)
            except ValueError, e:
                raise ValueError("Could not load the configuration file: %s" % e)
            return config
    except IOError:
        raise ValueError('Could not read the configuration file "%s".' % config_file_path)

def load_crawler(config):
    try:
        crawler_name = config['crawler']
    except KeyError:
        raise ValueError("Configuration must specify the name of the crawler to use.")

    try:
        crawler_args = config['args']
    except KeyError:
        raise ValueError("Configuration must specify the arguments to give to the crawler.")

    try:
        crawler_class = getattr(crawlers, crawler_name)
    except AttributeError:
        raise ValueError('Could not find a crawler named "%s".' % crawler_name)
    # This may trigger one of many exceptions.
    crawler = crawler_class(crawler_args)
    return crawler

def main():
    logger.info('RETINA Crawler starting..')
    if len(sys.argv) != 2:
        print "Usage: python main.py path/to/config.json"
        sys.exit(1)
    try:
        config = load_config(sys.argv[1])
    except ValueError, e:
        logger.error("There was a problem with the given configuration: %s." % e)
        sys.exit(-1)
    try:
        crawler = load_crawler(config)
    except ValueError, e:
        logger.error("There was a problem initializing the crawler with the given configuration: %s." % e)
        sys.exit(-1)

    logger.info('Loaded crawler "%s".' % crawler.__class__.__name__)
    logger.info("Running at %s" % time.ctime())
    
    try:
        # By design, crawl() should never throw an exception.
        while crawler.crawl():
            thread.sleep(1)
    except Exception, e:
        # This code should not be called and is considered a bug if it does.
        logger.exception(e)
        sys.exit(-1)
    # TODO: Handle early termination (Ctrl+C).

if __name__ == "__main__":
    main()
