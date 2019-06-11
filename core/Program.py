"""
Program.py
@author: byteface
"""

class Program(object):
	"""
    Program - this class loads a command and its meta
    """

	path=""
	program=""
	meta={}

 	def __init__(self,path,program):

		self.path = path
		self.program = program

		import _meta
		self.meta = _meta._meta( path )