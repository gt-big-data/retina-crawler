import article
from writers import PrintWriter, FileWriter
from RssFeedParser import RssLinkParser
import hashlib

def main():
	feed_parser = RssLinkParser("http://rss.cnn.com/rss/edition.rss")
	links = feed_parser.get_links()
	
	for link in links:
		article_info = article.create_article(link)
		article_data = article.article_dictionary(article_info)
		filename = hashlib.md5(article_data["title"]).hexdigest() + ".txt"
		writer = FileWriter(filename)
		writer.write(article_data)

if __name__ == "__main__":
	main()