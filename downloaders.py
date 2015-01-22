from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

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
            try:
                article.download_and_parse()
                self._writer.write(article.to_dict())
            except NotImplementedError:
                # We must of encountered a video article - just skip over it.
                logging.warning("Encountered an unparsable article: %s" % article.url)
            except IOError:
                logger.error("Could not download the following article: %s\nReason: %s" % (article.url, e))
            except ValueError, e:
                logging.error("Could not parse the article: %s\nReason: %s" % (article.url, e))
            except Exception, e:
                logging.exception("An unspecified error occurred while processing the URL: %s" % article.url)
        # Clear the queue when we finish.
        self._articles = []

def _run(article):
    """Download and process an article.

    This function is designed for use in multiprocess processing.

    Arguments:
    article -- The article to process.

    Return a JSON serializable dictionary of the article's data.
    """
    article.download_and_parse()
    return article.to_dict()

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

    def _write(self, article):
        """Internal method for writing parsed articles in the main thread.

        Arguments:
        article -- A dictionary to output
        """
        self._writer.write(article)

    def process_all(self):
        """Download, scrape, and print all queued articles."""
        with ProcessPoolExecutor(max_workers=self._threads) as executor:
            try:
                results = [executor.submit(_run, article) for article in self._articles]
                for future in as_completed(results):
                    self._write(future.result())
            except KeyboardInterrupt:
                executor.shutdown(wait=False)
                raise
        self._articles = []
