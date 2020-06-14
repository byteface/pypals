import shutil
import os
import json
from typing import *

from pypals.PyPal import PyPal


class PyWorld:

    def __init__(self, name: str):
        print("Who are you looking for?") if not name else None
        name_to_find = input("> ") if not name else name
        self.get_pypal_by_name(name_to_find)

    def get_pypal_by_name(self, name: str):
        pypal = "pypals/%s/" % name
        if name != "" and (os.path.exists(pypal) or os.path.islink(pypal)):
            pal = PyPal({'name': name})
            pal.welcome()
        else:
            self.create_new_pypal(name)

    def create_new_pypal(self, name: str):

        try:
            os.mkdir('pypals') # create empty dir for user pypals at cwd
        except:
            print('done!')


        pypal = "pypals/%s/" % name
        print(f"{name} doesn't exist, create them now? yes or no")
        is_new = input("> ")
        if(is_new[0].lower() == 'y'):
            print("Your name?")
            friend = input("> ")

            # create the new guy # - TODO - may need to write the files?

            # - TODO - may need to write the files? - ask who is my parent! . accepts list

            parent = "pypals/skeleton"
            new_pypal = f'pypals/{name}'
            # shutil.copytree(parent, new_pypal)

            # TODO- fix up later. just getting it working as pypi package for now
            try:
                os.mkdir(new_pypal) # create empty dir for user pypals at cwd
            except:
                print('done!')


            try:
                obj = {}
                obj['name'] = name
                obj['friend'] = friend
                data={}
                data['object'] = obj
                with open(f'{new_pypal}/_meta.json', 'w') as f:
                    json.dump(data, f)


                # TODO- fix up later. just getting it working as pypi package for now
                try:
                    os.mkdir(f'{new_pypal}/hello') # create empty dir for user pypals at cwd
                except:
                    print('done!')

                hello = """def run(o):
    print(f"Hello, to you { o.o['friend']}!")
    return True"""
                with open(f'{new_pypal}/hello/hello.py', 'w') as f:
                    f.write(hello)

            except Exception as e:
                print("Failed to create _meta.json")

            # load up your n00b!
            pal = PyPal({'name': name})
            pal.introduce()

        else:
            print("OK, bye for now")
            exit()