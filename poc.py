import CrawlerRunners
import sys
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logger = logging.getLogger('retina-crawler')

def main():
    runner = None
    logger.info('RETINA CRAWLER starting..')
    try:
        if len(sys.argv) < 2:
            runner = CrawlerRunners.SimpleRunner()
        else:
            config = None
            config_file_path = sys.argv[1]
            with open(config_file_path) as f:
                config = json.load(f)
            runner_type = getattr(CrawlerRunners, config['runner'])
            logger.info('loaded runner "{}"'.format(config['runner']))
            if 'args' in config:
                runner = runner_type(config['args'])
            else:
                runner = runner_type()
    except Exception, e:
        logger.error('Invalid config given, error is "{}"'.format(str(e)))
        sys.exit(-1)

    while True:
        try:
            logger.info('Running at {}'.format(time.time()))
            runner.run()
        except Exception, e:
            logger.error(str(e))
            time.sleep(0.5)


if __name__ == "__main__":
    main()
