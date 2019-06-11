"""
PyPal.py
@author: byteface
"""

class PyPal(object):
	"""
	main controller
    """

    # memory? - obj with funcitons for loading data etc.

	# dictionary that stores object from _meta.json
	o = None

	# TODO - if current context is gone should be able to go through history
	# MULTIPLE CONTEXT OBJECT MAY NEED TO EXISTS. searching for relevant ones is a requirement
	context=None

	# TODO - should every statement should carry certainty?. for now maybe store number 0-1 on here?
	#certainty=0 
	
	# TODO third person, you, actor???... you can 'be' another person
	#perspective={} 

	# the natural language processing engine. eventually will live on a brain object
	nlp=None # TODO - should be an array

	# natural language generation. used for output
	nlg=None # TODO - as above


	history=[] # TODO - should the history go on the context obj?


	def __init__(self,data):
		"""
		data param is obj with unique name. i.e {'name':'pypal'}
		"""
		import json
		with open("bin/%s/_meta.json" % data['name']) as json_file:
			self.o = json.load(json_file)['object']
		
		# TODO - externalise the class
		self.nlp=NLP( self )

		# TODO - externalise the class
		self.nlg=NLG( self )

		#self.context=Context( [self], [self] ) # talk to self


	def introduce(self):
		"""
		on create message
		"""
		self.nlg.say( "Hi my name is %s, Thankyou for creating me!" % self.o['name'] )
		self.listen()


	def welcome(self):
		"""
		welcome message
		"""
		self.nlg.say( "%s I see you have returned!" % self.o['friend'] )
		self.listen()


	def listen(self):
		"""
		listen loop
		"""
		try:
			self.nlg.say( "I am listening..." )
			information = input("> ")
			self.process( information )
			self.listen()
		except:
			self.nlg.log( "FAIL :::::listen" )
	


	## TODO - this should be a HEAR function and should process chunks
	# TODO - this is something that would be also good to parrallel process and decide which streams of informtion to listen to or ignore
	def process(self,information,caller=None,callee=None):

		self.context=Context( self, information ) # FOR NOW JUST FOR STORING PATHS

		self.history.append(information)

		# update the context object
		#self.context=Context( [caller], [callee] )

		# bust all into words, squash whitespace
		words = information.split(None)

		# if its a one letter answer. some helpers/shortcuts
		if len(words)==1:

			# added a repeat function
			if information == 'r':
				print( self.history[len(self.history)-2] )
				self.process( self.history[len(self.history)-2] )
				return

			# show command history
			if information == 'h':
				for h in history:
					print( h )
				return

			self.nlp.processOneWord( information )
			return

		self.nlp.processSentence( information )
		return


	# TODO - need to ask meaning of words. to at least put it into memory for considering
	# should also be able to check dictionary / nltk sources. but needs to build a program for the word
	def ask_word_meaning(self,word):

		self.nlp.say( "What is '%s'?" % word )
		answer = input("> ")

		# TODO - NO - should probs be processess response
		self.nlp.addNewWord( word, answer )



class Context(object):
	"""
	store caller, callee information
    """
	
	# both can be lists of animals
	caller=None
	callee=None

	# useful for commands to know where they are loading from
	# so can dump/store stuff there directly when scraping etc.

	#BASEPATH = './bin/%s/brain/commands/add/grades/files3' % o.o['name']
	#BASEPATH = './bin/%s/brain/commands/add/grades/files3' % o.o['name']
	BASEPATH=''

	# TODO - may move these 3 onto the NLP. and make context more of a caretaker pattern extended to surmise and store sessions.
	LAST_COMMAND =''
	COMMAND_PATH =''
	#PARAMS=''
	
	def __init__(self, parent, command, caller=None,callee=None):

		# self.caller=caller
		# self.callee=callee

		self.BASEPATH = './bin/%s/brain/commands' % parent.o['name']
		self.LAST_COMMAND = command

		path = '/'.join( self.LAST_COMMAND.split(' ') )
		file = '_'.join( self.LAST_COMMAND.split(' ') ) + '.py'

		self.COMMAND_PATH = '%s/%s' % ( self.BASEPATH, path )

		#self.PARAMS='' # NOTE - gets updated once string is parsed




class NLP(object):
	"""
    NLP are processes for word parsing. Generating functions for words.
    Essentially a custom module loader
    """
	owner=None
	
	# TODO -
	#TIME
	#PLACE

	#BASEPATH = './bin/%s/brain/commands/add/grades/files3' % o.o['name']


	def __init__(self,owner):
		self.owner=owner


	def addNewWord( self, word, answer ):
		# TODO - addNewWord. store what friend thinks/says it is
		return


	def processOneWord( self, word ):
		"""
		parse single word commands.
		basically runs a command from the command folder
		"""

		#TODO - check that the word is clean 
		#TODO - see if we know the word
		#TODO - deal with inuendo
		#TODO - lemmatiser maybe required. or we re-routing manually?

		knows_word=False;

		c_path = 'bin/%s/brain/commands' % self.owner.o['name']

		if self.has_command(c_path+"/"+word+"/"+word+".py"):	
			self.owner.nlg.log( "command detected" )
			knows_word=True
			return self.runWordAsFunction( c_path, word )

		if knows_word == False:
			self.owner.nlg.say( "I don't yet know that word" )



	# now that we know input function we can run it.. 
	# TODO - should probably create new problem though and process that way
	# TODO - all the meta properties need updating
	def runWordAsFunction(self,path,word):

		import sys
		sys.path.append( "%s/%s" % (path,word) )		

		try:

			# TODO - check and update all the meta props
			command_module = __import__( word )

			from importlib import reload
			reload(command_module) # reload class without restarting pypal

			return command_module.run(self.owner)

		except Exception(e):
			self.owner.nlg.say( "Sorry, I can't do that, I tried but it didn't work" )
			self.owner.nlg.log( "CHECK YOUR VIRUTAL ENVIRONMENT IS RUNNING." )
			pass


	# TODO - try to find the finite verb
	# NOTE - AT THE MOMENT ONLY PROCESSING COMMANDS
	def processSentence( self, sentence ):
		# print("processSentence")

		words = sentence.split(None)
		word_count = len(words)
		basepath = 'bin/%s/brain/commands' % self.owner.o['name']
		
		word_path_arr=[]

		# walk up the sentence
		for word in words:

			root = basepath+"/"+'/'.join(word_path_arr)
			has_path = self.has_path( root +"/"+ word )
			
			# if next word is the last word. check for a command and run it without params.
			if (len(word_path_arr)+1)==word_count:
				path = root+"/"+word
				function = '_'.join( word_path_arr ) + "_" + word
				if self.has_command(path+"/"+function+".py"):
					return self.runSentenceAsFunction( path, function )


			# if nowhere to go. but there's a command at current path. run it and pass the rest as param
			if (False==has_path):

				function = '_'.join( word_path_arr )

				if self.has_command(root+"/"+function+".py"):

					# get params by removing where we were up to
					params = sentence.replace( ' '.join( word_path_arr ), '' )

					# REMOVE THE WHITE SPACE FROM START OF PARAMS
					params = params[1:]

					# TODO - note. i see i built up to path to strip param. problem here is param is on the command_path. and doesn't get parsed off until here. during execution.
					# TODO - will have a rethink about how want context to work before changing this. so for now will operate on the context obj here
					# TODO - when doing change, nlp ref should probs get given to context. or context keeps them all in array.
					self.owner.context.COMMAND_PATH = self.owner.context.COMMAND_PATH.replace( params, '' )
					#self.owner.context.PARAMS = params

					# TODO - throw error if no param is passed
					if params == None or params == '':
						print('ERROR:parameter expected. none recieved')

					# run the function
					return self.runSentenceAsFunction( root, function, params )

				else:
					break

			word_path_arr.append(word)


		# TODO - if no command, attempt gnerating reponse from the self compiled programs.
		# TODO - integrate memory, world states, schemas and emotions

		return self.owner.nlg.say( "No command found" )



	# params at the moment are 'rest of string'
	# long term might break around finite verb and pass whole string?
	def runSentenceAsFunction(self,path,function,params=None):

		#print "runSentenceAsFunction"
		#print path, function, params

		import sys
		sys.path.append( path )

		try:

			# TODO - check all the meta props
			# TODO - may need to also write to some of the meta
			# TODO - if no meta create a default one

			command_module = __import__( function )

			from importlib import reload
			reload(command_module) # reload class without restarting pypal

			if(params!=None):
				return command_module.run(self.owner,params)
			else:
				return command_module.run(self.owner)

			pass

		except Exception(e):
			self.owner.nlg.log( "runSentenceAsFunction FAIL!! \
				\n happens when : \
				\n failing code in the command. i.e imports used by the command not intalled \
				\n venv not running \
				\n not passing params when required" )
			return False
			#self.owner.listen()
		
		pass


	# run several possibilities. decide which is most relevant?
	# the listener as to suppose an ontological truth in each word as they hear it
	# when that doesn't happen even over sets of words things have to be considered
	# and find more context or information. even lead to questioning
	def suppose():
		pass



	## ---------------------------- NLP LANGUGAGE UTILS -----------------------------------

	# check a lookup table of yes words. program needs to be able to expand that list
	# TODO - if one word use lookup, else use NLTK sentimement tool
	# NOTE - false DOES NOT MEAN it is negative, it could be neutral
	def is_string_positive( s ):
		pass

	# check a lookup table of no words. program needs to be able to expand that list
	# TODO - if one word use lookup, else use NLTK sentimement tool
	# NOTE - false DOES NOT MEAN it is positive, it could be neutral
	def is_string_negative( s ):
		pass

	# check a lookup table of 
	# TODO - building lookup tables on the fly is something we need to do
	# RETURN THE NUMBER OR WORD FALSE
	def is_string_number( s ):
		# TODO - check if NLTK can do this
		pass


	def is_math_operator():
		# TODO - check if NLTK can do this
		pass



	## ---------------------------- NLP FILE UTILS -----------------------------------

	# TODO - may get rid of this lookup and have root words as delegators
	def hasParams( self, path, word ):
		"""
		check if parameters True
		"""
		try:
			#TODO - shoud just check if folder has param folder
			import Program
			program = Program.Program( path, word );
			canHasParams = program.meta.get_property( 'rules', 'parameters' );
			return canHasParams
		
		except:
			print("no meta or param found")
			return False # force false if passing a non command. TODO- BUT. we shouldn't be calling if the case.


	def has_path( self, path_to_directory ):
		import os.path
		return os.path.isdir(path_to_directory)


	def has_command(self, path_to_py_file):
		import os.path
		return os.path.isfile(path_to_py_file)



class NLG(object):
	"""
    NLG - generates sentences in the natural language
    at moment just logs strings to output.
    from now on all output should come through here
    """	
	owner=None

	def __init__(self,owner):
		self.owner=owner

	def say( self, words ):
		"""
		output helps distinguish pypals when in the console
		"""
		print( "%s : %s" % ( self.owner.o['name'], words ) )
		return

	# TODO - setup python logger
	# TODO - pass ref to pypal?
	# TODO - logs should write to a file and be accessible by events. i.e. evt12345 - created variable xxx
	def log( self, words ):
		"""
		log differs to the 'say' method.
		log should be more about debugging.
		say should be user comms
		"""

		return # NOTE <<<<<<<<<<<<<<<<<<<<<< im not running

		# TOOD - if debug is true
		import logging
		logging.warning( "------------------------------------- %s : %s" % ( self.owner.o['name'], words ) )
		return



	def generate_random_sentence( self, words ):
		"""
		TODO - look at ways of generating random sentences.
		"""

		# 1.
		# think of model it's currently building.
		# think if it has any gaps on that model taht it would like to fill
		# interests. .. 'need to know'
		# what is x.

		self.say(  )
		return