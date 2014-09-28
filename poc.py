import article
from writers import PrintWriter, FileWriter, MongoWriter
from ArticleInserter import ArticleInserter
from RssFeedParser import RssLinkParser
import hashlib
import logging
import time

feeds = ["http://rss.cnn.com/rss/edition.rss", # world/national news
		"http://feeds.abcnews.com/abcnews/topstories",
		"http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml",
		"http://www.ajc.com/list/rss/news/local/news-georgia-and-region/aCxP/", # local news		
		"http://www.reddit.com/.rss", # entertainment
		"http://www.tmz.com/rss.xml",
		"http://sports.espn.go.com/espn/rss/news", # sports
		"http://online.wsj.com/xml/rss/3_7455.xml", # finance
		"http://feeds.feedburner.com/TechCrunch/", #tech
		"http://podcasts.engadget.com/rss.xml",
		"http://feeds.feedburner.com/hacker-news-feed?format=xml",
		]

def main():
	article_writer = MongoWriter()
	feed_parsers = [RssLinkParser(feed) for feed in feeds]
	while True:
		for feed_parser in feed_parsers:
			try:
				links = feed_parser.get_new_links()
				
				for link in links:
					article_info = article.create_article(link)
					article_data = article.article_dictionary(article_info)
					article_writer.write(article_data)
					time.sleep(0.1) # So we don't get blocked
			except Exception, e:
				logging.error(str(e))
				time.sleep(0.5)
		

if __name__ == "__main__":
	main()