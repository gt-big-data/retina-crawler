from article import Article

class ArticleDownloader(object):
    def __init__(self, url):
        """Create a LinkDownloader.

        Arguments:
        url -- The URL of the article to download.
        """
        self.url = url
        self.article = Article(url)

    def download_article(self):
        self.article.download_and_parse()
