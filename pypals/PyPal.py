import json
import sys
from importlib import reload
import logging
import os.path

from pypals.Program import Program

class PyPal(object):

    def __init__(self, data):
        """
        data : {'name':'pypal'}
        """
        with open(f"pypals/{data['name']}/_meta.json") as json_file:
            self.o = json.load(json_file)['object']

        self.history = []
        self.nlp = NLP(self)
        self.nlg = NLG(self)
        # self.context=Context( [self], [self] ) # talk to self
        # TODO - wont I need all these to not be class vars in long run so can parralelise?. this'll do for now.
        self.memory = Memory()

    def introduce(self):
        self.nlg.say(f"Hi, My name is {self.o['name']}, Thankyou for creating me!")
        self.listen()

    def welcome(self):
        self.nlg.say(f"{self.o['friend']} I see you have returned!")
        self.listen()

    def listen(self):
        try:
            self.nlg.say("I'm listening...")
            information = input("> ")
            self.process(information)
            self.listen()
        except Exception as e:
            self.nlg.log("FAIL :::::listen")

    def process(self, information: str, caller=None, callee=None):
        self.context = Context(self, information)
        self.history.append(information)

        words = information.split(None)
        if len(words) == 1:

            # helpers/shortcuts
            # show history
            if information is 'h':
                for h in self.history:
                    print(h)
                return

            # repeat last command
            if information is 'r':
                print(self.history[len(self.history)-2])
                self.process(self.history[len(self.history)-2])
                return

            # do it
            self.nlp.processOneWord(information)
            return

        self.nlp.processSentence(information)
        return

    def create_command(self, command: str):        
        folders = command.split(" ")
        filepath = f"pypals/{self.o['name']}/"
        for folder in folders:
            try:
                filepath += f"/{folder}"
                os.mkdir(filepath)
            except Exception as e:
                # print(e)
                pass

        print(f"What should the default response be?")
        default = input("> ")

        try:
            # gen the meta
            data={}
            data["object"]={}
            data["rules"]={"parameters":"False","redirect":"False"}
            data["events"]=[]
            data["stats"]={"hitcount":"0"}
            with open(f'{filepath}/_meta.json', 'w') as f:
                json.dump(data, f)

            func = f"""def run(o):
    print('running: {default}')
    return '{default}'"""

            cmd = "_".join(folders) + ".py"
            with open(f'{filepath}/{cmd}', 'w') as f:
                f.write(func)

        except:
            print('failed to create folders!')


# TODO - see if I can use inspection to get the callee so don't have to pass context. tho i think that just gets the class name?
# - also then you couldn't write to a different context. (inspection could set it as the default if non passed?)
class Memory(object):

    def __init__(self):
        pass

    def create(self, context=None, data=None, filename: str = "model.json"):
        f = open(context.COMMAND_PATH + '/' + filename, "w")
        f.write(json.dumps(data))
        f.close()

    def read(self, context=None, filename: str = "model.json"):
        f = open(context.COMMAND_PATH + '/' + filename, "r")
        data = json.loads(f.read())
        return data

    # def update(self, data=None, filename="model.json" ):
    #     pass

    # def delete(filename="model.json"):
    #     pass

    # def relate
    # create binding to the memory blobs in other commands for access here?


class Context(object):

    BASEPATH = ''
    LAST_COMMAND = ''
    COMMAND_PATH = ''
    # PARAMS=''

    def __init__(self, parent, command: str, caller=None, callee=None):

        # self.caller=caller
        # self.callee=callee

        Context.BASEPATH = './pypals/%s' % parent.o['name']
        Context.LAST_COMMAND = command

        path = '/'.join(self.LAST_COMMAND.split(' '))
        file = '_'.join(self.LAST_COMMAND.split(' ')) + '.py'

        self.COMMAND_PATH = '%s/%s' % (Context.BASEPATH, path)
        # self.PARAMS='' # NOTE - gets updated once string is parsed


class NLP(object):

    # TODO -
    # TIME
    # PLACE

    def __init__(self, owner):
        self.owner = owner

    def processOneWord(self, word: str):
        """
        runs a single word command from the command folder
        """
        c_path = f"pypals/{self.owner.o['name']}"
        if self.has_command(c_path+"/"+word+"/"+word+".py"):
            self.owner.nlg.log("command detected")
            return self.runWordAsFunction(c_path, word)
        
        self.owner.nlg.say("I don't know that command!")
        print(f"Do you want me to create the command: {word}")
        is_new_command = input("> ")
        if(is_new_command[0].lower() == 'y'):
            self.owner.create_command(word)


    def runWordAsFunction(self, path: str, word: str):
        sys.path.append("%s/%s" % (path, word))
        try:
            command_module = __import__(word)
            reload(command_module)  # reload class without restarting pypal
            return command_module.run(self.owner)

        except Exception as e:
            print('failed::')
            print(e)

            pass

    # TODO - try to find the finite verb
    # NOTE - AT THE MOMENT ONLY PROCESSING COMMANDS
    def processSentence(self, sentence: str):
        words = sentence.split(None)
        word_count = len(words)
        basepath = f"pypals/{self.owner.o['name']}"
        word_path_arr = []

        # walk up the sentence
        for word in words:

            root = basepath+"/"+'/'.join(word_path_arr)
            has_path = self.has_path(root + "/" + word)

            # if next word is the last word. check for a command and run it without params.
            if (len(word_path_arr)+1) == word_count:
                path = root+"/"+word
                function = '_'.join(word_path_arr) + "_" + word
                if self.has_command(path+"/"+function+".py"):
                    return self.runSentenceAsFunction(path, function)

            # if nowhere to go. but there's a command at current path. run it and pass the rest as param
            if (False == has_path):

                function = '_'.join(word_path_arr)

                if self.has_command(root+"/"+function+".py"):

                    # get params by removing where we were up to
                    params = sentence.replace(' '.join(word_path_arr), '')

                    # REMOVE THE WHITE SPACE FROM START OF PARAMS
                    params = params[1:]

                    # TODO - note. i see i built up to path to strip param. problem here is param is on the command_path. and doesn't get parsed off until here. during execution.
                    # TODO - will have a rethink about how want context to work before changing this. so for now will operate on the context obj here
                    # TODO - when doing change, nlp ref should probs get given to context. or context keeps them all in array.
                    self.owner.context.COMMAND_PATH = self.owner.context.COMMAND_PATH.replace(
                        params, '')
                    #self.owner.context.PARAMS = params

                    # TODO - throw error if no param is passed
                    if params == None or params == '':
                        print('ERROR:parameter expected. none recieved')

                    # run the function
                    return self.runSentenceAsFunction(root, function, params)

                else:
                    break

            word_path_arr.append(word)

        # TODO - if no command, attempt gnerating reponse from the self compiled programs.
        # TODO - integrate memory, world states, schemas and emotions

        self.owner.nlg.say("No command found")
        print(f"Do you want me to create the command: {word}")
        is_new_command = input("> ")
        if(is_new_command[0].lower() == 'y'):
            self.owner.create_command(sentence)

        return

    # params at the moment are 'rest of string'
    # long term might break around finite verb and pass whole string?
    def runSentenceAsFunction(self, path: str, function: str, params=None):
        sys.path.append(path)
        try:

            command_module = __import__(function)
            reload(command_module)  # reload class without restarting pypal

            if(params != None):
                return command_module.run(self.owner, params)
            else:
                return command_module.run(self.owner)

        except Exception as e:
            print('runSentenceAsFunction failed::')
            print(e)
    #         self.owner.nlg.log("runSentenceAsFunction FAIL!! \
            # \n happens when : \
            # \n failing code in the command. i.e imports used by the command not intalled \
            # \n venv not running \
            # \n not passing params when required")

        pass

    # def suppose():
    # def reason():

    # ---------------------------- NLP LANGUGAGE UTILS -----------------------------------

    # check a lookup table of yes words. program needs to be able to expand that list
    # TODO - if one word use lookup, else use NLTK sentimement tool
    # NOTE - false DOES NOT MEAN it is negative, it could be neutral

    def is_string_positive(self,s):
        pass

    # check a lookup table of no words. program needs to be able to expand that list
    # TODO - if one word use lookup, else use NLTK sentimement tool
    # NOTE - false DOES NOT MEAN it is positive, it could be neutral
    def is_string_negative(self,s):
        pass

    # check a lookup table of
    # TODO - building lookup tables on the fly is something we need to do
    # RETURN THE NUMBER OR WORD FALSE
    def is_string_number(self,s):
        # TODO - check if NLTK can do this
        pass

    def is_math_operator(self,s):
        # TODO - check if NLTK can do this
        pass

    # ---------------------------- NLP FILE UTILS -----------------------------------

    # TODO - may get rid of this lookup and have root words as delegators

    def hasParams(self, path: str, word: str) -> bool:
        try:
            program = Program.Program(path, word)
            canHasParams = program.meta.get_property('rules', 'parameters')
            return canHasParams
        except Exception as e:
            print("no meta or param found")
            # force false if passing a non command. TODO- BUT. we shouldn't be calling if the case.
            return False

    def has_path(self, path_to_directory: str) -> bool:
        return os.path.isdir(path_to_directory)

    def has_command(self, path_to_py_file: str) -> bool:
        return os.path.isfile(path_to_py_file)


class NLG(object):

    def __init__(self, owner):
        self.owner = owner

    def talk(self, comment: str):
        import subprocess
        subprocess.call(["say", comment])
        pass

    def say(self, comment: str):
        print(comment)
        pass

    def log(self, comment: str, filename: str = "log.json"):
        """
        # TODO - setup python logger
        # TODO - logs should write to a file and be accessible by events. i.e. evt12345 - created variable xxx
        """

        # Context.BASEPATH
        #     f = open(context.BASEPATH + '/' + filename, "w")
        #     f.write(json.dumps(data))
        #     f.close()

        return  # NOTE <<<<<<<<<<<<<<<<<<<<<< im not running

    # TODO
    # def generate_random_sentence(self, words):
