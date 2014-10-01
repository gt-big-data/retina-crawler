import feedparser

class MultiRSSLinkParsers(object):
    def __init__(self, rss_feed_urls):
        self._rssLinkParsers = [RssLinkParser(feed) for feed in rss_feed_urls]

    def get_new_links(self):
        outLinks = []
        for parser in self._rssLinkParsers:
            outLinks.extend(parser.get_new_links())
        return outLinks

class RssLinkParser(object):
    def __init__(self, rss_url):
        self.etag = None
        self.rss_url = rss_url

    def get_new_links(self):
        feed = feedparser.parse(self.rss_url, etag = self.etag)
        if 'etag' in feed:
            self.etag = feed.etag
        links = []
        for entry in feed.entries:
            links.append(entry.link)
        return links
