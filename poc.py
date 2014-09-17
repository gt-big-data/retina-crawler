import article
from writers import PrintWriter, FileWriter
from RssFeedParser import RssLinkParser
import hashlib
import newspaper
import feedfinder

def get_all_the_feeds():
	for url in newspaper.popular_urls():
		rss_feeds = feedfinder.feeds(url)
		for rss_feed in rss_feeds:
			process_url(rss_feed)

def process_url(url):
	feed_parser = RssLinkParser(url)
	links = feed_parser.get_links()
	
	for link in links:
		article_info = article.create_article(link)
		article_data = article.article_dictionary(article_info)
		filename = hashlib.md5(article_data["title"]).hexdigest() + ".txt"
		writer = FileWriter(filename)
		writer.write(article_data)

def main():
	process_url("http://rss.cnn.com/rss/edition.rss")

if __name__ == "__main__":
	main()