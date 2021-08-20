"""
    pypals
    ====================================

    pypals now has a cli interface. check __main__.py for usage

"""

__version__ = "1.0.2"

class DefaultCommands():
    """ default commands that come with first pypal """

    HELLO = """def run(o, *args, **kwargs):
    print(f"Hello, to you { o.o['friend']}!")
    return True
    """
    
    QUIT = """def run(o, *args, **kwargs):
    import sys
    sys.exit(0)
    """

    # copilot generated commands
    # ASSERT = """def run(o, *args, **kwargs):
    # if not args:
    #     print("You must provide a condition to assert")
    #     return False
    # if args[0] == "True":
    #     print("Assertion was true")
    #     return True
    # else:
    #     print("Assertion was false")
    #     return False
    # """
    
    # COMPLAINT = """def run(o, *args, **kwargs):
    # print(f"I'm sorry, {o.o['friend']}, I'm afraid I can't do that.")
    # return False
    # """
    
    # AFFIRMATIVE = """def run(o, *args, **kwargs):
    # print("affirmative")
    # return True
    # """

    # NEGATIVE = """def run(o, *args, **kwargs):
    # print("negative")
    # return False
    # """


class Utils():

    @staticmethod
    def y_n(x):
        """ returns a boolean for any given input """
        if isinstance(x, bool):
            return x
        elif isinstance(x, (int, float)):
            return bool(x)
        elif isinstance(x, str):
            reply = x.lower()
            if reply.lower() in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep", "sure", "ok", "go ahead", "certainly", "do", "1", "too right"]:
                return True
            elif reply.lower() in ['nah', "no", "nope", "n", "dont", "0", "nop", "naa", "naaa"]:
                return False

            if 'y' in x[0].lower():
                return True
            elif 'n' in x[0].lower():
                return False
        else:
            raise ValueError(f"{x} is not a valid input")


class DocsMixin():

    def generate_docs_for_pypal(self):
            self.nlg.say(f"generate_docs_for_pypal...")

            import os
            # full depth search on all directories to build a list of any .py files
            # files = []
            # for root, dirs, files in os.walk(f'pypals/{self.o["name"]}'):
            #     for file in files:
            #         if file.endswith('.py'):
            #             files.append(os.path.join(root, file))
            # use Pathlib to get the full path of all python files in all directories at full depth
            from pathlib import Path
            files = list(Path('pypals/{}'.format(self.o["name"])).glob('**/*.py'))
            # print(files)

            # create the docs
            self.nlg.say(f"Creating docs...")
            from domonic.html import html, head, body, div, h1, h2, p, a, button
            from domonic.html import input as input_
            page = html(head(),body(
                h1('Hi, my name is ' + self.o['name']),
                p(f"Here's a list of your current commands..."),
                div(_id="docs")))
            page.getElementById("docs").innerHTML = ""
            for f in files:
                # read the contents of the file
                content = open(f, 'r').read()
                # exract take the 2nd and 3rd lines from the file
                content = content.split('\n')[1:3]
                docs = page.getElementById("docs")
                docs += div(
                    h2(f),
                    div(
                        p(content,_id=f"{f}",),
                        _id="output"
                    )
                #       button('run'),
                #       button('delete')
                    )
            with open(f'pypals/{self.o["name"]}/_docs.html', 'w') as f:
                f.write(str(page))
            self.nlg.say(f"Docs created!")
            return True


    @staticmethod
    def generate_docs_list_pypals():
            print(f"generate_docs_list_pypals...")
            # list the directories in only the pypals directory
            import os
            pypals = os.listdir('pypals')
            # only show the directories
            pypals = [x for x in pypals if os.path.isdir(f'pypals/{x}')]
            # print(pypals)
            # remove pycache
            pypals = [x for x in pypals if not x.endswith('__pycache__')]


            # create the docs
            print(f"Creating docs...")
            from domonic.html import html, head, body, div, h1, h2, p, a, button, code, sub, br
            from domonic.html import input as input_
            page = html(head(),body(
                h1('This is a list of your current pypals:'),
                div(_id="docs")))
            page.getElementById("docs").innerHTML = ""
            for pal in pypals:
                docs = page.getElementById("docs")
                docs += div(
                    h2(pal),
                    p( f"To talk to {pal} do :", br(), code(f"python3 -m pypals {pal}")),
                    sub( '! Remember to start your virtual environment ;)'),
                )
            #page.getElementsByTagName('body').append(div(
            #    div("", _id="feedback")
            with open(f'pypals/_docs.html', 'w') as f:
                f.write(str(page))
            print(f"Docs created!")
            return True
