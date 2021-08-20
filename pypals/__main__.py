"""
    pypal CLI
    ====================================
    - how you interact with your pypals
"""

import argparse
import os
import json
from pathlib import Path
from rich import print

from .PyPal import PyPal
from . import DefaultCommands, __version__, Utils, DocsMixin

PYPALS_DIR = 'pypals' # TODO - pypal should also reference this value

def get_pypal_by_name(name: str, command: str=None):
    # create a dir to store pypals if not already there
    if not Path(PYPALS_DIR).exists():
        try:
            os.mkdir(PYPALS_DIR)
        except Exception as e:
            print(f'Failed to created {PYPALS_DIR} directory!', e)
    # returns the pypal or creates one if it doesn't exist
    pypal = f"{PYPALS_DIR}/{name}/"
    if name != "" and (os.path.exists(pypal) or os.path.islink(pypal)):
        pal = PyPal({'name': name})
        if command is None:
            pal.welcome()
        else:
            try:
                pal.process(command)
            except Exception as e:
                print(e)
    else:
        create_new_pypal(name)


def create_new_pypal(name: str):
    pypal = f"{PYPALS_DIR}/{name}/"
    print(f"{name} does not exist. Would you like to create them now?")
    if Utils.y_n(input("> ")):
        print("What is your name?")
        friend = input("> ")
        new_pypal = f'{PYPALS_DIR}/{name}'
        if not Path(new_pypal).exists():
            os.mkdir(new_pypal)
            try:
                obj = {}
                obj['name'] = name
                obj['friend'] = friend
                data = {}
                data['object'] = obj
                with open(f'{new_pypal}/_meta.json', 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                print("Failed to create pypal:", e)

            # create the default commands
            try:
                os.mkdir(f'{new_pypal}/hello')
                with open(f'{new_pypal}/hello/hello.py', 'w') as f:
                    f.write(DefaultCommands.HELLO)
            except Exception as e:
                print('Failed to create hello command!', e)

            try:
                os.mkdir(f'{new_pypal}/quit')
                with open(f'{new_pypal}/quit/quit.py', 'w') as f:
                    f.write(DefaultCommands.QUIT)
            except:
                print('Failed to create quit command!', e)
        
        pal = PyPal({'name': name})
        pal.introduce()

    else:
        print("OK! bye for now :wave:")
        exit()


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, prog="pypals", usage="%(prog)s [options]", description="terminal buddies")
    parser.add_argument('-l', '--list', help="displays a list all your pypals", action='store_true')
    parser.add_argument('-h', '--help', action='store_true')  # shows help in the terminal
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-d', '--docs', help="generate a _docs file to list all your pypals", action='store_true')

    # args = parser.parse_args()
    args, name = parser.parse_known_args()
    return args, name


def do_things(arguments, name):
    if arguments.list is True:
        # list all pypals in the pypals directory using os.listdir
        print("listing all pypals")
        print(os.listdir("pypals"))
        return
    if arguments.help is True:
        print("Here's a list of the available commands. You can also pass a pypals name")
        print('-h, --help')
        print('-v, --version')
        print('-l, --list')
        print('-d, --docs')
        return
    if arguments.version is True:
        print(__version__)
        return __version__
    if arguments.docs is True:
        DocsMixin.generate_docs_list_pypals()
        return

    # runs if no arguments are passed
    command = None
    if name is None or len(name) == 0:
        print("Who are you looking for?")
        name = input("> ")
    elif isinstance(name, list):
        if len(name) > 1:
            command = name[1]
        name = name[0]
    get_pypal_by_name(name, command)


if __name__ == "__main__":
    args, name = parse_args()
    do_things(args, name)