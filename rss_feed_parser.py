import feedparser
import urlparse
from article import Article
import time
import logging
from datetime import datetime

class RssFeedParser(object):
    def __init__(self, rss_url):
        self.etag = None
        self.rss_url = rss_url
        self.etag_filename = self._get_filename(rss_url)
        self.feed_update_count = 0
        self._previous_entries = {}

        try:
            with open(self.etag_filename) as old_etag_file:
                etag = old_etag_file.read()
                if etag:
                    self.etag = etag
        except:
            pass

    def _get_filename(self, rss_url):
        p = urlparse.urlparse(rss_url)
        path_parts = [part for part in p.path.split('/') if part]
        path_formatted = '-'.join(path_parts)
        return '{domain}.{path}.etag'.format(
            domain=p.netloc,
            path=path_formatted
        )

    def _save_etag(self, etag):
        self.etag = etag
        with open(self.etag_filename, 'w+') as etag_file:
            etag_file.write(etag)

    def _deduplicate_entries(self, rss_entries):
        return max(rss_entries, key=lambda entry: entry.published_parsed)

    def _unique_entries_by_link(self, rss_entries):
        rss_entries_by_link = {}

        for entry in rss_entries:
            if entry.link in rss_entries_by_link:
                rss_entries_by_link[entry.link].append(entry)
            else:
                rss_entries_by_link[entry.link] = [entry]

        for link, rss_entries in rss_entries_by_link.iteritems():
            selected_entry = self._deduplicate_entries(rss_entries)
            yield link, selected_entry

    def _filter_new(self, entries):
        for link, entry in entries:
            if link not in self._previous_entries:
                yield link, entry
                self._previous_entries[link] = set([entry.published_parsed])
            elif entry.published_parsed not in self._previous_entries[link]:
                yield link, entry
                self._previous_entries[link].add(entry.published_parsed)

    def get_new_articles(self):
        resp = feedparser.parse(self.rss_url, etag = self.etag)

        if resp.status == 304: # Not modified
            if 'etag' in resp:
                raise Exception('ERR_NO_MOD_ETAG,Updated etag should not happen when the resource was not modified.')
            return []

        if 'etag' not in resp:
            return []

        if self.etag == resp.etag:
            raise Exception('ERR_MOD_ETAG_NOT_MOD,resource modified, but etag not modified.')

        self._save_etag(resp.etag)
        self.feed_update_count += 1

        new_articles = []
        for link, entry in self._filter_new(self._unique_entries_by_link(resp.entries)):
            article = Article(link)
            new_articles.append(article)

        logging.info('{_type},{time},{feed},{update_count},{num_entries},{new_entries}'.format(
                _type='RSS_UPDATE',
                time=time.time(),
                feed=self.rss_url,
                update_count=self.feed_update_count,
                num_entries=len(resp.entries),
                new_entries=len(new_articles)
            )
        )

        return new_articles

class MultipleRSSFeedParser(object):
    def __init__(self, feeds):
        self._parsers = [RssFeedParser(feed) for feed in feeds]

    def get_new_articles(self):
        new_articles = []
        for parser in self._parsers:
            new_articles.extend(parser.get_new_articles())
        return new_articles
