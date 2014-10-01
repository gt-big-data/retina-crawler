from article_downloader import ArticleDownloader
from multiprocessing import Pool

class SingleThreadedDownloader(object):
	def __init__(self, writer):
		self._downloaders = []
		self._writer = writer

	def queue_link(self, link):
		self._downloaders.append(ArticleDownloader(link))

	def download_all(self):
		for downloader in self._downloaders:
			downloader.download_article()
			self._writer.write(downloader.article)

def _run(args):
	downloader, writer = args
	downloader.download_article()
	writer.write(downloader.article)

class MultiProcessDownloader(object):
	def __init__(self, writer):
		self._downloaders = []
		self._writer = writer

	def queue_link(self, link):
		self._downloaders.append((ArticleDownloader(link), self._writer))

	def download_all(self):
		# TODO Make the number of threads/processes configurable.
		p = Pool(4)
		p.map(_run, self._downloaders)
