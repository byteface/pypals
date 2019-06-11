"""
PyWorld.py
@author: byteface
"""

class PyWorld:
	"""
   	Class for loading PyPals
    """
	def __init__(self,name):
		"""
		$ python PyWorld.py - to create a new pypal
		$ python PyWorld.py pypal - to quick load a specific pypal
		"""
		print( "who are you looking for?" ) if not name else None
		name_to_find = input("> ") if not name else name
		self.get_pal_by_name(name_to_find)


	def get_all_pals(self):
		# TODO - load all the pals from the bin and list them < ls shortcut
		for pal in self.pals:
			print(pal)


	def get_pal_by_name(self,name):
		"""
		looks in the /bin returns the pypal, if requested doesn't exists ask to create
		"""
		URI = "bin/%s/" % name
		
		print(URI)

		import os
		if name!="" and ( os.path.exists( URI ) or os.path.islink( URI ) ):
			obj={'name':name}
			from core.PyPal import PyPal
			pal = PyPal(obj)
			pal.welcome()
		else:
			self.createNewPal( name )


	def createNewPal(self,name):
		"""
		creates pypals
		"""

		URI = "bin/%s/" % name

		print( name + " doesn't exist, create them now? yes or no" )
		isNewUser = input("> ")
		if(isNewUser=='yes'): # TODO - sentiment or library of 'yes' words				

			print("your name?")
			friend = input("> ")

			# create the new guy
			import shutil
			import os
			TEMPLATE = "bin/skeleton"
			NEW_PAL = 'bin/%s' % name
			shutil.copytree(TEMPLATE, NEW_PAL)

			# here we add new pal name to the meta data
			try:
				import json
				with open( '%s/_meta.json' % NEW_PAL ) as meta:
					data = json.load(meta)
					obj = data['object']
					obj['name'] = name
					data['object'] = obj
				# re-write new file our data
				with open('%s/_meta.json' % NEW_PAL,'w') as new_file:
					json.dump(data, new_file)
			except:
				print("Failed to create new _meta.json")

			obj={'name':name}

			# load up your n00b!
			from core.PyPal import PyPal
			pal = PyPal(obj)
			pal.introduce()

		else:
			print("OK, bye for now")
			exit()