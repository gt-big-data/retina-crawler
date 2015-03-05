import pymongo
import sys

class UpdateVersion():

    def __init__(self):
        self.m = pymongo.MongoClient("146.148.59.202", 27017)
        self.db = self.m.big_data

    def add_version_number(self, number):
        doc = {"_id" : "version",
                "number" : number}
        self.db.articles.insert(doc)

    def update_version_number(self, number):
        query = {"_id" : "version"}
        self.db.articles.update(query, {"number" : number})

    def get_version_number(self):
        query = {"_id" : "version"}
        doc = self.db.articles.find_one(query)
        return doc["number"]

u = UpdateVersion()
num = sys.argv[0]
u.update_version_number(num)