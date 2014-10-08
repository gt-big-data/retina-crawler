import json
import pymongo
import sys
import hashlib
import os
from article import Article
from bson.objectid import ObjectId

class PrintWriter(object):
    """Class for writing JSON data to the screen."""

    def __init__(self):
        pass

    def write(self, article):
        """Write an Article object to the screen.

        Arguments:
        article -- A JSON-serializable article.
        """
        print json.dumps(article.__dict__, indent=4, ensure_ascii=False)

class FileWriter(object):
    """Class for writing JSON data to a file."""

    def __init__(self):
        check_and_make_dir("./test_files/")

    def write(self, article):
        """Write an Article object to a file.

        Arguments:
        article -- A JSON-serializable article.
        """
        filepath = "test_files/" + hashlib.md5(article.__dict__["title"]).hexdigest() + ".json"
        pretty_string = json.dumps(article.__dict__, indent=4)
        with open(filepath, 'w') as output_file:
            output_file.write(pretty_string)

def check_and_make_dir(path):
    '''Makes dir with given path, unless if it already exists.'''
    try:
        os.mkdir(path)
    except OSError:
        pass

class MongoWriter():
    def __init__(self, host, port):
      self.m = pymongo.MongoClient(host, port)
      self.db = self.m.big_data

    def write(self, article):
        """Write an Article object to MongoDB.

        Arguments:
        article -- A JSON-serializable article.
        """
        #try:
        html_id = ObjectId()
        article_dict = {
            'v' : '0.0.1',
            'url' : article.url,
            'source_domain' : article.source_domain,
            'text' : article.text,
            'title' : article.title,
            'download_date' : article.download_date,
            'authors' : article.authors,
            'categories' : article.categories,
            'keywords' : article.keywords,
            'images' : article.images,
            'location' : article.location,
            'summary' : article.summary,
            'suggested_articles' : article.suggested_articles,
            'meta_lang' : article.meta_lang,
            'meta_favicon' : article.meta_favicon,
            'pub_date' : article.pub_date,
            'html_key' : html_id,
        }

        html_dict = {
            'id' : html_id,
            'data' : article.html
        }

        self.db.articles.insert(article_dict)
        self.db.html.insert(html_dict)
        #except:
        #    print("Unexpected error:", sys.exc_info()[0])
