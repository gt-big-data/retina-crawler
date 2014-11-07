from urlparse import urlparse
import newspaperdef _get_favicon(doc):    return _get_data(doc, path=["link"], selector={'rel':'shortcut icon'}, field='href')[0]def _get_selector(selector):    pairs = (u"@%s='%s'" % (k, v) for k,v in selector.iteritems())
    return u"[%s]" % (" and ".join(pairs))def _get_meta(doc, selector, first=True):    """Get metadata from the html.    Arguments:    doc -- The HTML element to grab metadata from.    first -- True if the first result should be automatically returned.    selector -- A dictionary of html selectors.    Examples:    _get_meta(doc, {'name':'news_keywords'})    _get_meta(doc, {'property':'article:modified'})    Return a list of all elements that match the selectors or just the first one.    """    result = _get_data(doc, path=["meta"], selector=selector, field="content")    if first:        return result[0]    else:        return resultdef _get_data(doc, path=[], selector=None, field=None):    """    Get all Elements at the given path.    Arguments:    doc -- The HTML element to extract data from.    path -- A list of the path components to the desired element.    Examples:    _get_data(doc, ["body", "article", "p"])    Return a list of all elements that match the path.    """    path_text = u"//%s" % "//".join(path)    if selector is not None:        selector_text = _get_selector(selector)    else:        selector_text = ""    if field is not None:        field_text = u"/@%s" % field    else:        field_text = u""        return doc.xpath(u"%s%s%s" % (path_text, selector_text, field_text))
def parse_cnn_article(article, doc):    if _get_meta(doc, {'name': 'medium'}) == "video":        raise NotImplementedError("Cannot parse a video article.")    text = _get_data(doc, ["body", "div", "div", "div", "p"])    text = u"\n".join(t.text for t in text if t.text is not None)    article.text = text    article.title = _get_meta(doc, {'itemprop': 'headline'})    article.categories = [_get_meta(doc, {'itemprop': 'articleSection'})]    article.categories.extend(_get_meta(doc, {'itemprop': 'subsection'}, first=False))    article.pub_date = _get_meta(doc, {'itemprop': 'dateModified'})    article.authors = _get_meta(doc, {'itemprop': 'author'})    article.location = _get_meta(doc, {'itemprop': 'contentLocation'})    article.summary = _get_meta(doc, {'itemprop': 'description'})    # Page doesn't link to a favicon so just assume the default.    article.meta_favicon = "http://www.cnn.com/favicon.ico"    article.meta_lang = _get_meta(doc, {'itemprop': 'inLanguage'})    # location is sometimes not provided.    if article.location == "":        article.location = None    # CNN doesn't provide any keywords. Use categories instead.    article.keywords = article.categories

def parse_nytimes_article(article, doc):    if _get_meta(doc, {'name': 'CG'}) == "Video":
        raise NotImplementedError("Cannot parse a video article.")    text = _get_data(doc, ["body", "article", "p"])    text = u"\n".join(t.text for t in text if t.text is not None)    article.text = text    article.title = _get_meta(doc, {'property': 'og:title'})    keywords = _get_meta(doc, {'name': "news_keywords"})    article.keywords = keywords.split(';')    article.pub_date = _get_meta(doc, {'property': 'article:modified'})    article.authors = _get_meta(doc, {'name': 'author'}, first=False)    #Not always present    try:        article.location = _get_meta(doc, {'name': 'geo'})    except:        article.location = None    article.summary = _get_meta(doc, {'itemprop': 'description'})    article.meta_favicon = _get_favicon(doc)    article.meta_lang = _get_meta(doc, {'itemprop': 'inLanguage'})    article.categories = [_get_meta(doc, {'itemprop': 'articleSection'})]
    #TODO: Get title image out of the article.    #TODO: Get suggested articles out of the article.def newspaper_parser(article):    newspaper_article = newspaper.build_article(article.url)
    newspaper_article.download()
    newspaper_article.parse()
    article.text = newspaper_article.text
    article.title = newspaper_article.title
    article.html = newspaper_article.html

    # Optional parameters
    if newspaper_article.authors:
        article.authors = newspaper_article.authors
    else:
        article.authors = None

    # Not sure how to implement right now
    article.category = None

    # Merge keywords and meta_keywords into the same param
    article.keywords = []
    if newspaper_article.keywords:
        article.keywords = newspaper_article.keywords
    if newspaper_article.meta_keywords:
        article.keywords = list(set(article.keywords + newspaper_article.meta_keywords))

    if article.keywords == ['']:
        article.keywords = None

    if newspaper_article.images:
        article.images = newspaper_article.images
    else:
        article.images = None

    # Will implement later
    article.location = None

    if newspaper_article.summary:
        article.summary = newspaper_article.summary
    else:
        article.summary = None

    # Not sure how to implement
    article.suggested_articles = None

    if newspaper_article.meta_favicon:
        article.meta_favicon = newspaper_article.meta_favicon
    else:
        article.meta_favicon = None

    if newspaper_article.meta_lang:
        article.meta_lang = newspaper_article.meta_lang
    else:
        article.meta_lang = None

    if newspaper_article.published_date:
        article.pub_date = newspaper_article.published_date
    else:
        article.pub_date = None