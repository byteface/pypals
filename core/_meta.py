"""
_meta.py
@author: byteface
"""

class _meta(object):
	"""
    parser to the meta.json on each object
    """


    # TODO - may get rid in favour of a config obj with regular python vars. setup on the commands

	path=None
	data=None

	def __init__( self, path ):
		""" meta for each object. initialised by Program passes the path """
		self.path = path

		import json
		with open(self.path+"/_meta.json") as json_file:
			# print("open file")
			self.data = json.load(json_file)


	def get(self,meta_type):
		""" getter for json nodes """
		return self.data[meta_type]


	def get_property(self,meta_type,prop):
		""" getter for props on json nodes """
		return self.data[meta_type][prop]


	# TODO - these can be merged and *args, **kwargs