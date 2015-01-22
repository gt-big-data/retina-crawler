from datetime import date
from urlparse import urlparse
import newspaper
from opengraph import OpenGraph

def _sanity_check(article):
    """Check that all required fields in the article have been filled in.

    Throw a ValueError if anything is missing.
    """
    # The syntax `if not <var>:` takes care of None, empty strings, and empty lists.
    # This should absolutely never be missing but just in case.
    if not article.url:
        raise ValueError("URL is missing.")
    if not article.download_date:
        raise ValueError("Download date is missing.")
    if not article.html:
        raise ValueError("HTML is missing.")
    if not article.source_domain:
        raise ValueError("Source domain is missing.")

    if not article.title:
        raise ValueError("Title is missing.")
    if not article.summary:
        raise ValueError("Summary is missing.")
    if not article.text:
        raise ValueError("Text is missing.")

    # For now, require a published date or reject the article.
    if not article.pub_date:
        raise ValueError("Published date is missing.")

def _get_favicon(doc):
    return _get_data(doc, path=["link"], selector={'rel':'shortcut icon'}, field='href')[0]

def _get_selector(selector):
    pairs = (u"@%s='%s'" % (k, v) for k,v in selector.iteritems())
    return u"[%s]" % (" and ".join(pairs))

def _get_meta(doc, selector, first=True):
    """Get metadata from the html.

    Arguments:
    doc -- The HTML element to grab metadata from.
    first -- True if the first result should be automatically returned.
    selector -- A dictionary of html selectors.

    Examples:
    _get_meta(doc, {'name':'news_keywords'})
    _get_meta(doc, {'property':'article:modified'})
    Return a list of all elements that match the selectors or just the first one.
    """
    try:
        result = _get_data(doc, path=["meta"], selector=selector, field="content", first=first)
    except Exception:
        return None

def _get_data(doc, path=[], selector=None, field=None, first=False):
    """
    Get all Elements at the given path.

    Arguments:
    doc -- The HTML element to extract data from.
    path -- A list of the path components to the desired element.

    Examples:
    _get_data(doc, ["body", "article", "p"])

    Return a list of all elements that match the path.
    """
    path_text = u"//%s" % "//".join(path)

    if selector is not None:
        selector_text = _get_selector(selector)
    else:
        selector_text = ""

    if field is not None:
        field_text = u"/@%s" % field
    else:
        field_text = u""

    try:
        result = doc.xpath(u"%s%s%s" % (path_text, selector_text, field_text))
        if first:
            return result[0]
        else:
            return result
    except Exception:
        return None

def _parse_schema_org(article, doc):
    if _get_meta(doc, {'name': 'medium'}) == "video":
        raise NotImplementedError("Cannot parse a video article.")

    article.title = article.title or _get_meta(doc, {'itemprop': 'headline'})
    article.categories = article.categories or [_get_meta(doc, {'itemprop': 'articleSection'})]
    # Sub categories would be nice, but are a bit difficult to grab right now.
    #article.categories.extend(_get_meta(doc, {'itemprop': 'subsection'}, first=False))
    article.pub_date = article.pub_date or _get_meta(doc, {'itemprop': 'dateModified'})
    article.authors = article.authors or [_get_meta(doc, {'itemprop': 'author'})]
    article.location = article.location or _get_meta(doc, {'itemprop': 'contentLocation'})
    article.summary = article.summary or _get_meta(doc, {'itemprop': 'description'})
    article.meta_lang = article.meta_lang or _get_meta(doc, {'itemprop': 'inLanguage'})

def _parse_open_graph(article):
    og = OpenGraph(html=article.html)
    if not og.is_valid():
        return

    if og["type"] != "article":
        raise NotImplementedError("Cannot parse a OG type: %s" % og["type"])

    og.setdefault(None)

    article.title = article.title or og.get("title")
    article.summary = article.summary or og.get("description")
    article.images = article.images or [og.get("image")]
    article.meta_lang = article.meta_lang or og.get("locale")
    article.keywords = article.keywords or og.get("tag")
    article.categories = article.categories or [og.get("category")]
    article.authors = article.authors or [og.get("author")]
    article.pub_date = article.pub_date or og.get("modified_date")

def _parse_newspaper(article):
    newspaper_article = newspaper.build_article(article.url)
    newspaper_article.set_html(article.html)
    newspaper_article.parse()
    article.text = article.text or newspaper_article.text
    article.title = article.title or newspaper_article.title
    article.authors = article.authors or newspaper_article.authors
    if not article.keywords:
        keywords = newspaper_article.keywords or []
        other_keywords = newspaper_article.meta_keywords or []
        article.keywords = list(set(keywords + other_keywords))
    article.images = article.images or newspaper_article.images
    article.summary = article.summary or newspaper_article.summary
    article.meta_favicon = article.meta_favicon or newspaper_article.meta_favicon
    article.meta_lang = article.meta_lang or newspaper_article.meta_lang
    article.pub_date = article.pub_date or newspaper_article.published_date

def _parse_extra(article, doc):
    article.meta_favicon = article.meta_favicon or article.source_domain + "/favicon.ico"
    article.keywords = article.keywords or article.categories
    article.pub_date = article.pub_date or _get_data(doc, path=[".//time"], field="datetime", first=True)

    # If all else fails, get the published day (not time) from the URL.
    try:
        year = date.today().year
        pieces = article.url.split("/%d/" % year)[1].split("/")
        month = pieces[0]
        day = pieces[0]
        article.pub_date = article.pub_date or "%d-%s-%s" % (year, month, day)
    except Exception:
        # I give up - Take the download date.
        article.pub_date = str(article.pub_date or article.download_date)

    #TODO: Get title image out of the article.
    #TODO: Get suggested articles out of the article.

def parse_article(article, doc):
    # Each parser will only update fields if there is no data already.
    # Note that the final newspaper parser is the only one that finds text.
    _parse_open_graph(article)
    _parse_schema_org(article, doc)
    _parse_newspaper(article)
    _parse_extra(article, doc)
    _sanity_check(article)
