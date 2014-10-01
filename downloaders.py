from article_downloader import ArticleDownloader

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
