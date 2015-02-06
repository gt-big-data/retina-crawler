from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

def process(article):
    """Return True if the article should be written. If it returns False, something
    will have been logged.
    """
    try:
        article.download_and_parse()
        return article
    except NotImplementedError:
        # We must of encountered a video article - just skip over it.
        logging.warning("Encountered an unparsable article: %s" % article.url)
    except IOError:
        logger.error("Could not download the following article: %s\nReason: %s" % (article.url, e))
    except ValueError, e:
        logging.error("Could not parse the article: %s\nReason: %s" % (article.url, e))
    except Exception, e:
        logging.exception("An unspecified error occurred while processing the URL: %s" % article.url)
    return None

class SingleThreadedDownloader(object):
    """Class for downloading and parsing links in a single (current) thread."""

    def __init__(self, writer):
        """Create a new SingleThreadedDownloader.

        Arguments:
        writer -- The writer to output the crawled articles with.
        """
        self._articles = []
        self._writer = writer

    def queue_article(self, article):
        """Queue an article for processing at a later time.

        Arguments:
        article -- The article to process when `process_all` is called.
        """
        self._articles.append(article)

    def process_all(self):
        """Download, scrape, and print all queued articles."""
        for article in self._articles:
            self._writer.write(article)
        # Clear the queue when we finish.
        self._articles = []

class MultiProcessDownloader(object):
    def __init__(self, threads, writer):
        self._articles = []
        self._writer = writer
        self._threads = threads

    def queue_article(self, article):
        """Queue an article for processing at a later time.

        Arguments:
        article -- The article to process when `process_all` is called.
        """
        self._articles.append(article)

    def process_all(self):
        """Download, scrape, and print all queued articles."""
        with ProcessPoolExecutor(max_workers=self._threads) as executor:
            try:
                results = [executor.submit(process, article) for article in self._articles]
                for future in as_completed(results):
                    article = future.result()
                    if article:
                        self._writer.write(article)
            except KeyboardInterrupt:
                executor.shutdown(wait=False)
                raise
        self._articles = []
