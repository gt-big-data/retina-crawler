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
        article -- A JSON-serializable dictionary.
        """
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
        filepath = "test_files/" + hashlib.md5(article["title"]).hexdigest() + ".json"
        pretty_string = json.dumps(article, indent=4)
        with open(filepath, 'w') as output_file:
            output_file.write(pretty_string)

def check_and_make_dir(path):
    '''Makes dir with given path, unless if it already exists.'''
    try:
        os.mkdir(path)
    except OSError:
        pass

class MongoWriter():
    def __init__(self, host, port, max_pool_size):
      self.m = pymongo.MongoClient(host, port, max_pool_size)
      self.db = self.m.big_data

    def write(self, article):
        """Write an Article object to MongoDB.

        Arguments:
        article -- A JSON-serializable dictionary.
        """
        article['v'] = '0.0.3'

        self.db.articles.insert(article)
