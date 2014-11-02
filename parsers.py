from urlparse import urlparse
import re

def parse_cnn_article(article):
    parsed_url = urlparse(article.url)

    #the "edition" subdomain is not relevant in this case
    article.source_domain = parsed_url.netloc.replace("edition.", "");

    #these locations in the path represent categories
    article.categories = parsed_url.path.split("/")[4:-1]

YEAR_REGEXP = re.compile('^20([1-9]){2}$')

def parse_nytimes_categories(url):
    '''
    URLs have a "redirect" part of the path, which is 2nd to last in the path
    (last is /story.htm). The redirect part consists of
    nytimes / YYYY / MM / DD / category / article-name (if has category)
    OR
    subdomain.nytimes / YYYY / MM / DD / article-name (if this is a "blog" article)
    '''
    redirect_part = urlparse(url).path.split('/')[-2]
    redirect_pieces = redirect_part.replace('0A', '0')\
        .replace('0L', '')\
        .replace('0B', '.')\
        .replace('0E', '-')\
        .replace('0C0D', '?')\
        .replace('0G', '&')\
        .replace('0F', '=')\
        .replace('0C', '/')\
        .split('/')

    for i, word in enumerate(redirect_pieces):
        if YEAR_REGEXP.match(word) and i + 3 < len(redirect_pieces) - 1:
            return [redirect_pieces[i + 3]]
    return None

def parse_nytimes_article(article):
    article.categories = parse_nytimes_categories(article.url)
