from multiprocessing import Pool

class SingleThreadedDownloader(object):
    def __init__(self, writer):
        self._articles = []
        self._writer = writer

    def queue_article(self, article):
        self._articles.append(article)

    def process_all(self):
        for article in self._articles:
            article.download_and_parse()
            self._writer.write(article)
        self._articles = []

def _run(args):
    article, writer = args
    article.download_and_parse()
    writer.write(article)

class MultiProcessDownloader(object):
    def __init__(self, threads, writer):
        self._articles = []
        self._writer = writer
        self._threads = threads

    def queue_article(self, article):
        self._articles.append((article, self._writer))

    def process_all(self):
        p = Pool(self._threads)
        p.map(_run, self._articles)
