from urlparse import urlparse
from Article import Article

def parse_cnn_article(article):
        parsedurl = urlparse(url)

        #the "edition" subdomain is not relevant in this case
        article.source_domain = parse.netloc.replace("edition.", "");

        #these locations in the path represent categories
        article.categories = parse.path.split("/")[4:6]
