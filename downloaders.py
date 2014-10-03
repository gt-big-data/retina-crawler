from article_downloader import ArticleDownloader
from multiprocessing import Pool

class SingleThreadedDownloader(object):
    def __init__(self, writer):
        self._downloaders = []
        self._writer = writer

    def queue_link(self, link):
        self._downloaders.append(ArticleDownloader(link))

    def process_all(self):
        for downloader in self._downloaders:
            downloader.download_article()
            self._writer.write(downloader.article)

def _run(args):
    downloader, writer = args
    downloader.download_article()
    writer.write(downloader.article)

class MultiProcessDownloader(object):
    def __init__(self, threads, writer):
        self._downloaders = []
        self._writer = writer
        self._threads = threads

    def queue_link(self, link):
        self._downloaders.append((ArticleDownloader(link), self._writer))

    def process_all(self):
        p = Pool(self._threads)
        p.map(_run, self._downloaders)
