import json
import sys
from importlib import reload
import logging
import os.path

from rich import print

from pypals.Program import Program

from . import Utils
from . import _meta

class PyPal(object):

    def __init__(self, data):
        """
        data : {'name':'pypal'}
        """
        _meta._meta.BAK = data
        self.o = _meta._meta(f"pypals/{data['name']}/")

        self.history = []
        self.nlp = NLP(self)
        self.nlg = NLG(self)
        # self.context=Context( [self], [self] ) # talk to self
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
            if information == 'h':
                for h in self.history:
                    print(h)
                return

            # repeat last command
            if information == 'r':
                print(self.history[len(self.history)-2])
                self.process(self.history[len(self.history)-2])
                return

            # quit
            if information == 'q':
                self.nlg.say("Goodbye :wave:")
                sys.exit()

            # list commands
            if information == 'l':
                for cmd in os.listdir(f'pypals/{self.o["name"]}'):
                    print(cmd)
                return

            # list all config variables in this pypals config
            if information == 'c':
                for key in self.o.keys():
                    print(key)
                return
            
            # convert the config file to a preffered format
            if information.startswith('c='):
                self.o.save_as(information.split('=')[1])
                return

            # show stats
            if information == 'stats':
                print(self.o['stats'])
                return
            
            # show memory
            # if information == 'm':
                # print(self.memory)
                # return

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

            func = f"""def run(o, *args, **kwargs):
    print(f'running: {default}')
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
        # self.data = {}
        pass

    def create(self, context=None, data=None, filename: str = "model.json"):
        f = open(context.COMMAND_PATH + '/' + filename, "w")
        f.write(json.dumps(data))
        f.close()

    def read(self, context=None, filename: str = "model.json"):
        f = open(context.COMMAND_PATH + '/' + filename, "r")
        data = json.loads(f.read())
        return data

    def update(self, context=None, data=None, filename: str = "model.json"):
        f = open(context.COMMAND_PATH + '/' + filename, "w")
        f.write(json.dumps(data))
        f.close()
    
    def delete(self, context=None, filename: str = "model.json"):
        os.remove(context.COMMAND_PATH + '/' + filename)
    
    
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
        if self.has_command(f"{c_path}/{word}/{word}.py"):
            # self.owner.nlg.log("command detected")
            return self.runWordAsFunction(c_path, word)
        
        self.owner.nlg.say("I don't know that command!")
        print(f"Do you want me to create the command?: {word}")
        if Utils.y_n(input("> ")):
            self.owner.create_command(word)


    def runWordAsFunction(self, path: str, word: str):
        sys.path.append(f"{path}/{word}")
        try:
            command_module = __import__(word)
            reload(command_module)  # reload class without restarting pypal
            return command_module.run(self.owner)
        except Exception as e:
            print('failed::', e)
            return 'failed'


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
            has_path = os.path.isdir(root + "/" + word)

            # if next word is the last word. check for a command and run it without params.
            if (len(word_path_arr)+1) == word_count:
                path = root + "/" + word
                function = '_'.join(word_path_arr) + "_" + word
                if self.has_command(f"{path}/{function}.py"):
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
                    self.owner.context.COMMAND_PATH = self.owner.context.COMMAND_PATH.replace(params, '')
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

        self.owner.nlg.say("command not found")
        print(f"Do you want me to create the command?: {sentence}")
        if Utils.y_n(input("> ")):
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
            print('runSentenceAsFunction failed::', e)
            print("This can happen when :")
            print("Failing code in your command. i.e imports used by the command not intalled")
            print("Maybe your venv is not running?")
            # print("not passing params when required")


    # def suppose():
    # def reason():

    # ---------------------------- NLP LANGUGAGE UTILS -----------------------------------

    def word_to_number(self, numberword: str):
        # take a string for example 'five' and returns the number 5
        # TODO - make this more robust
        numberword = numberword.lower()
        
        return {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
            'ten': 10,
            'eleven': 11,
            'twelve': 12,
            'thirteen': 13,
            'fourteen': 14,
            'fifteen': 15,
            'sixteen': 16,
            'seventeen': 17,
            'eighteen': 18,
            'nineteen': 19,
            'twenty': 20,
            'thirty': 30,
            'forty': 40,
            'fifty': 50,
            'sixty': 60,
            'seventy': 70,
            'eighty': 80,
            'ninety': 90
        }.get(numberword, None)

    def number_to_word(self, number: int):
        # take a number and returns the word equivalent
        # TODO - make this more robust
        return {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine',
            10: 'ten',
            11: 'eleven',
            12: 'twelve',
            13: 'thirteen',
            14: 'fourteen',
            15: 'fifteen',
            16: 'sixteen',
            17: 'seventeen',
            18: 'eighteen',
            19: 'nineteen',
            20: 'twenty',
            30: 'thirty',
            40: 'forty',
            50: 'fifty',
            60: 'sixty',
            70: 'seventy',
            80: 'eighty',
            90: 'ninety'
        }.get(number, None)

    '''
    def phrase_to_math_operator(self, phrase: str):
        # take a string for example 'plus' and returns the math operator '+'
        # TODO - make this more robust
        return {
            'plus': '+',
            'minus': '-',
            'divided': '/',
            'multiplied': '*'
            # inlucde more here
            'modulus': '%',
            'times': '*',
            'divide': '/',
            # add other ways of saying it here
            'take away': '-',
            'divided by': '/',
            'add': '+',
            'added to': '+',
        }.get(phrase, None)


    def math_operator_to_phrase(self, phrase: str):
        # take a string for example 'plus' and returns the math operator '+'
        # TODO - make this more robust
        return {
            'plus': '+',
            'minus': '-',
            'divided': '/',
            'multiplied': '*'
        }.get(phrase, None)

    def phrase_to_function(self, phrase: str):
        raise NotImplementedError
        # match phrases to functions
        # take a phrase for example 'how many' and returns the function len()
        # TODO - make this more robust
        # return {
            # 'how many': len,
            # 'how much': sum,
            # 'what': lambda x: x,
            # 'what is the average of': lambda x: sum / len,
    '''

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

    def log(self, comment: str, filename: str = None):
        """
        # TODO - logs should be accessible by multilpe event keys. i.e. evt12345 x
        """
        if filename is None:
            filename =  self.owner.context.LAST_COMMAND + ".log"

        FORMAT = '{"t":"%(asctime)s","m":%(message)s}'
        #{ "t":"2006-02-08 22:20:02", "d":"data goes here", "uid": }
        logpath = self.owner.context.COMMAND_PATH + '/' + filename
        logging.basicConfig(filename=logpath, format=FORMAT, level=logging.DEBUG)
        # logging.debug(comment)
        logging.info(comment)
        # logging.warning(comment)
        return
