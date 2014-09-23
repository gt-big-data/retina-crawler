import article
from writers import PrintWriter, FileWriter
from RssFeedParser import RssLinkParser
import hashlib
import logging
import time

def main():

	while True:
		feed_parser = RssLinkParser("http://rss.cnn.com/rss/edition.rss")
		try:
			links = feed_parser.get_links()
			
			for link in links:
				article_info = article.create_article(link)
				article_data = article.article_dictionary(article_info)
				filename = hashlib.md5(article_data["title"]).hexdigest() + ".txt"
				writer = FileWriter(filename)
				writer.write(article_data)
		except Exception, e:
			logging.error(str(e))
			time.sleep(0.5)
		

if __name__ == "__main__":
	main()