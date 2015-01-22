import crawlers
from writers import DB_VERSION

import sys
import json
import logging
import time

def load_config(config_file_path):
    """Load a JSON configuration file.

    Raise a `ValueError` if the file could not be found or read for any reason.

    Arguments:
    config_file_path -- A path to the desired JSON file.

    Return a dictionary of key-value pairs from the config file.
    """
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
    """Create a crawler from configuration data.

    Raise a `ValueError` if the crawler cannot be created for any reason.

    Arguments:
    config -- A dictionary of configuration parameters for the crawler.

    Return a fully initialized crawler.
    """
    try:
        crawler_name = config['crawler']
    except KeyError:
        raise ValueError("Configuration must specify the name of the crawler to use.")

    try:
        crawler_args = config['args'] if 'args' in config else {}
    except KeyError:
        raise ValueError("Configuration must specify the arguments to give to the crawler.")

    try:
        crawler_class = getattr(crawlers, crawler_name)
    except AttributeError:
        raise ValueError('Could not find a crawler named "%s".' % crawler_name)
    # This may trigger one of many ValueErrors.
    if len(crawler_args) == 0:
        crawler = crawler_class()
    else:
        crawler = crawler_class(crawler_args)
    return crawler

def main():
    if len(sys.argv) != 2:
        print "Usage: python main.py path/to/config.json"
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('retina-crawler')
    logger.info('RETINA Crawler starting..')

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
    logger.info("Writing with DB version: %s" % DB_VERSION)

    while True: #TODO(): try-except properly everywhere / do a service
        try:
            continue_crawling = True
            while continue_crawling:
                start = time.time()
                continue_crawling = crawler.crawl()
                logger.info(str(time.ctime()) + ":Finished a round of crawling.")
                # Track how long crawling took and make sure it doesn't run more frequently than once per minute.
                end = time.time()
                if end - start < 60.0:
                    time.sleep(15.0)
                else:
                    continue
        # Handle early termination (Ctrl+C)
        except KeyboardInterrupt:
            logger.info("Terminating early by user request.")
            sys.exit(1)
        except Exception, e:
            # This code should not be called and is considered a bug if it does.
            logger.exception(e)
            time.sleep(5.0) #TODO():
    logger.critical("WE ESCAPED THE WHILE(TRUE) LOOP!!! What happened!?!?")

if __name__ == "__main__":
    main()
