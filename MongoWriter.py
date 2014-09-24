import pymongo
import sys


class MongoWriter():

    def __init__(self, host="localhost", port=27017):
      self.m = pymongo.MongoClient(host, port)
      self.db = self.m.retina

    def insert_article(self, article):
        try:
            self.db.crawlerarticles.insert(article)
        except:
            print("Unexpected error:", sys.exc_info()[0])