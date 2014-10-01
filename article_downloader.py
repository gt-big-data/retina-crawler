import article

class ArticleDownloader(object):
    def __init__(self, url):
		"""Create a LinkDownloader.
		
		Arguments:
		url -- The URL of the article to download.
		"""
		self.url = url
		self.article = None

	def download_article(self):
		article_info = article.create_article(self.url)
		article_data = article.article_dictionary(article_info)
		self.article = article_data