import json
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
	def __init__(self):
		pass

	def write(self, json_data):
		"""Write a JSON serializable object to a file.

		Arguments:
		json_data -- A JSON serializable object.
		"""
		filename = hashlib.md5(json_data["title"]).hexdigest() + ".txt"
		pretty_string = json.dumps(json_data, indent=4)
		with open(filename, 'w') as output_file:
			output_file.write(pretty_string)
