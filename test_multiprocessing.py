from rss_feed_parser import RssFeedParser
from multiprocessing import Pool
from writers import MongoWriter
import time

def run(art):
    art.download_and_parse()
    return art

def write(args):
    art, host, port = args
    writer = MongoWriter(host, port)
    writer.write(art)
    return True

def main():
    start = time.time()
    f = RssFeedParser('http://rss.cnn.com/rss/cnn_topstories.rss')
    arts = f.get_new_articles()
    p = Pool(5)
    parsed = p.map(run, arts)
    print 'fetched', len(arts), 'in ', time.time() - start, 'seconds'
    start = time.time()
    p.map(write, [(art, 'localhost', 27017) for art in parsed])
    print 'wrote', len(arts), 'in ', time.time() - start, 'seconds'


if __name__ == '__main__':
    main()
