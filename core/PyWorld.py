import shutil
import os
import json

from core.PyPal import PyPal

from typing import *
from enum import Enum


class PyWorld:

    def __init__(self, name: str):
        """
        $ python PyWorld.py - to create a new pypal
        $ python PyWorld.py pypal - to quick load a specific pypal
        """
        print("Who are you looking for?") if not name else None
        name_to_find = input("> ") if not name else name
        self.get_pypal_by_name(name_to_find)

    def get_pypal_by_name(self, name: str):
        pypal = "bin/%s/" % name
        if name != "" and (os.path.exists(pypal) or os.path.islink(pypal)):
            pal = PyPal({'name': name})
            pal.welcome()
        else:
            self.create_new_pypal(name)

    def create_new_pypal(self, name: str):
        pypal = "bin/%s/" % name
        print(name + " doesn't exist, create them now? yes or no")
        is_new = input("> ")
        if(is_new == 'yes' or 'y' or 'Yes' or 'Y'):
            print("Your name?")
            friend = input("> ")

            # create the new guy
            parent = "bin/skeleton"
            new_pypal = 'bin/%s' % name
            shutil.copytree(parent, new_pypal)

            try:
                with open('%s/_meta.json' % new_pypal) as f:
                    data = json.load(f)
                    obj = data['object']
                    obj['name'] = name
                    obj['friend'] = friend
                    data['object'] = obj
                with open('%s/_meta.json' % new_pypal, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                print("Failed to create new _meta.json")

            # load up your n00b!
            pal = PyPal({'name': name})
            pal.introduce()

        else:
            print("OK, bye for now")
            exit()
