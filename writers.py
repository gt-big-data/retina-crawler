import json
import pymongo
import sys
import hashlib

class PrintWriter(object):
	"""Class for writing JSON data to the screen."""
	def __init__(self):
		pass

	def write(self, json_data):
		"""Write a JSON serializable object to the screen.

		Arguments:
		json_data -- A JSON serializable object.
		"""
		print json.dumps(json_data, indent=4, ensure_ascii=False)

class FileWriter(object):
	"""Class for writing JSON data to a file."""

	def write(self, json_data):
		"""Write a JSON serializable object to a file.

		Arguments:
		json_data -- A JSON serializable object.
		"""
		filepath = hashlib.md5(json_data["title"]).hexdigest() + ".txt"
		pretty_string = json.dumps(json_data, indent=4)
		with open(filepath, 'w') as output_file:
			output_file.write(pretty_string)

class MongoWriter():

    def __init__(self, host="localhost", port=27017):
      self.m = pymongo.MongoClient(host, port)
      self.db = self.m.retina

    def write(self, article):
        try:
            self.db.CrawledArticles.insert({'hello' : 'world'})
        except:
            print("Unexpected error:", sys.exc_info()[0])

