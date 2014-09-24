import json
import pymongo
import sys

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
	def __init__(self, filepath):
		self._filepath = filepath

	def write(self, json_data):
		"""Write a JSON serializable object to a file.

		Arguments:
		json_data -- A JSON serializable object.
		"""
		pretty_string = json.dumps(json_data, indent=4)
		with open(self._filepath, 'w') as output_file:
			output_file.write(pretty_string)

class MongoWriter():

    def __init__(self, host="localhost", port=27017):
      self.m = pymongo.MongoClient(host, port)
      self.db = self.m.retina

    def write(self, article):
        try:
            self.db.crawlerarticles.insert(article)
        except:
            print("Unexpected error:", sys.exc_info()[0])