from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, as_completed

class SingleThreadedDownloader(object):
    def __init__(self, writer):
        self._articles = []
        self._writer = writer

    def queue_article(self, article):
        self._articles.append(article)

    def process_all(self):
        try:
            for article in self._articles:
                try:
                    article.download_and_parse()
                    self._writer.write(article.to_dict())
                except Exception e:
                    print("bad article")
                    print(e)
            self._articles = []
        except TypeError:
            raise ValueError("'articles' must be ")

def _run(article):
    article.download_and_parse()
    return article.to_dict()

class MultiProcessDownloader(object):
    def __init__(self, threads, writer):
        self._articles = []
        self._writer = writer
        self._threads = threads

    def queue_article(self, article):
        self._articles.append(article)

    def _write(self, article):
        self._writer.write(article)
    
    def process_all(self):
        with ProcessPoolExecutor(max_workers=self._threads) as executor:
            try:
                results = [executor.submit(_run, article) for article in self._articles]
                for future in as_completed(results):
                    self._write(future.result())
            except KeyboardInterrupt:
                executor.shutdown(wait=False)
                raise
