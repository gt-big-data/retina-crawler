import json
import pymongo
import sys
import hashlib
import os
from article import Article
from bson.objectid import ObjectId

DB_VERSION = '0.0.7'

class PrintWriter(object):
    """Class for writing JSON data to the screen."""

    def write(self, article):
        """Write an Article object to the screen.

        Arguments:
        article -- A JSON-serializable dictionary.
        """
        # Cannot JSON serialize a datetime object.
        article["download_date"] = str(article["download_date"])
        print json.dumps(article, indent=4, ensure_ascii=False)

class FileWriter(object):
    """Class for writing JSON data to a file."""

    def __init__(self):
        check_and_make_dir("./test_files/")

    def write(self, article):
        """Write an Article object to a file.

        Arguments:
        article -- A JSON-serializable dictionary.
        """
        # Cannot JSON serialize a datetime object.
        article["download_date"] = str(article["download_date"])
        try:
            filepath = "test_files/" + hashlib.md5(article["title"].encode("ascii", "ignore")).hexdigest() + ".json"
            pretty_string = json.dumps(article, indent=4)
            with open(filepath, 'w') as output_file:
                output_file.write(pretty_string)
        except:
            print article["title"]
            raise

def check_and_make_dir(path):
    """Makes a directory if it doesn't already exist.

    Arguments:
    path -- The path to try creating.
    """
    try:
        os.mkdir(path)
    except OSError:
        pass

class MongoWriter():
    def __init__(self, host, port):
      self.m = pymongo.MongoClient(host, port)

    def write(self, article):
        """Write an Article object to MongoDB.

        Arguments:
        article -- An article!
        """
        db = self.m.big_data
        html = article.html
        html_id = ObjectId()

        article_doc_updates = {
            'authors' : article.authors,
            'categories' : article.categories,
            'images' : article.images,
            'keywords' : article.keywords,
            'location' : article.location,
            'meta_favicon' : article.meta_favicon,
            'meta_lang' : article.meta_lang,
            'recent_download_date' : article.download_date,
            'recent_pub_date' : article.pub_date,
            'source_domain' : article.source_domain,
            'suggested_articles' : article.suggested_articles,
            'summary' : article.summary,
            'text' : article.text,
            'title' : article.title,
            'url' : article.url,
            'v' : DB_VERSION
        }

        article_doc_history = {
            'history' : {
                'download_date' : article.download_date,
                'html_id' : html_id,
                'pub_date' :  article.pub_date
            }
        }

        html_doc = {
            '_id' : html_id,
            'html' : html
        }

        db.articles.update(
            {'url' : article.url},
            {
                '$set' : article_doc_updates,
                '$push' : article_doc_history,
                '$inc' : {'history_len' : 1}
            },
            upsert=True
        )
        db.html.insert(html_doc)
