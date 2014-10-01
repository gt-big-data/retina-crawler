from RssFeedParser import RssLinkParser
from downloaders import *
from writers import *

def find_articles(url):
	feed_parser = RssLinkParser(url)
	links = feed_parser.get_links()
	return links

def main():
	links = find_articles("http://rss.cnn.com/rss/edition.rss")
	downloader = SingleThreadedDownloader(FileWriter())
	for link in links:
		downloader.queue_link(link)

	downloader.download_all()

if __name__ == "__main__":
	main()
