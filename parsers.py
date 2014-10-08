from urlparse import urlparse

def parse_cnn_article(article):
        parsed_url = urlparse(article.url)

        #the "edition" subdomain is not relevant in this case
        article.source_domain = parsed_url.netloc.replace("edition.", "");

        #these locations in the path represent categories
        article.categories = parsed_url.path.split("/")[4:-1]
        
