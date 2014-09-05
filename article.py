import newspaper


def create_article(article_url):
    article = newspaper.build_article(article_url)
    article.download()
    article.parse()
    return article
