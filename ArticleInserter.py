class ArticleInserter():

    def __init__(self, object, feed):
        self.writer = object
        self.feed = feed

    def findArticle():
        try:
            links = self.feed.get_links()

            for link in links:
                article_info = article.create_article(link)
                article_data = article.article_dictionary(article_info)
                filename = hashlib.md5(article_data["title"]).hexdigest() + ".txt"
                self.writer.write(article_data)
                time.sleep(0.1)

        except Exception, e:
            logging.error(Str(e))
            time.sleep(0.5)
