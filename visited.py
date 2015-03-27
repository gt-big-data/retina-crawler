from datetime import datetime
import logging
LOGGER = logging.getLogger('retina-crawler')


class VisitedTracker(object):

    def is_visited(self, url):
        pass

    def mark_visited(self, url):
        pass


class MemoryVistedTracker(VisitedTracker):

    def __init__(self, MAX=5000):
        self._cache = {}
        self._mru = []
        self._max = MAX

    def is_visited(self, url):
        return url in self._cache

    def _evict(self, n=1):
        LOGGER.info('MemoryVisitedTracker,Now evicting {} items..'.format(n))
        old_urls = sorted(iter(self._cache.items()), key=lambda x: x[1])[:n]
        for url, date in old_urls:
            del self._cache[url]

    def mark_visited(self, url, insert_time=None):
        insert_time = insert_time or datetime.now()
        if url in self._cache:
            self._cache[url] = insert_time
            return

        if len(self._cache) > self._max:
            self._evict(self._max // 10)

        self._cache[url] = url
