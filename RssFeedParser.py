import feedparser

etag  = None
class RssLinkParser(object):
    def __init__(self, rss_url):
        self.etag = None
        self.rss_url = rss_url

    def get_new_links(self):
        feed = feedparser.parse(self.rss_url, etag = self.etag)
        if 'etag' in feed:
            self.etag = feed.etag
        links = []
        print feed.entries[0].keys()
        for entry in feed.entries:
            links.append(entry.link)
        return links
