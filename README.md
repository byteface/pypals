<h1 align="center">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTe1LJtuvY4cuG7yN2ib3IYmFRU7nayGL3cDYSS8ckTrykpnRgJ&usqp=CAU"
    style="background-color:rgba(0,0,0,0);" height=230 alt="pypals: it really does nothing!">
    <br>
    pypals
    <br>
    <sup><sub><sup>Turn python snippets into command line buddies!</sup></sub></sup>
    <br>
</h1>

Keeps your python scripts and snippets as command line pals.

[![PyPI version](https://badge.fury.io/py/pypals.svg)](https://badge.fury.io/py/pypals.svg)

[![Downloads](https://pepy.tech/badge/pypals)](https://pepy.tech/project/pypals)


## installation
Get the package from pypi i.e.

	$ python3 -m pip install pypals --upgrade


see screen shot in archive folder for using pypal in vscode terminal


## usage
Sometimes you write code maybe to do some random job or snippet, scrape something, send a tweet, whatever.

It's useful to keep those bits of odd code somewhere. pypals are easy to remember ages later.

	$ python3 -m pypals sportsfan
	$ sportsfan doesn't exist, create them now? yes or no
	$ > yes
	$ your name?
	$ > mike
	$ Hi my name is sportsfan, Thankyou for creating me!
	$ I am listening...

sportsfan has been created for you in a /pypals directory. He can gather data about sports using any python commands you write and put in that folder

now try running this command...

	$ hello

now look in pypals/sportsfan/hello/hello.py file to see an example of a command.

To create commands try typing 'do something' at the prompt.

You will see it creates it for you. You can now just edit the file created and fill it in with your code.

Next try typing 'quit'

If you're editing a command you don't need to restart pypal. It will reload the command. You can even type 'r' to rerun it at the prompt.


### parameters
pass any words after your command it will pick them up as parameters.

when creating a command it will ask you what to type as a response, you can put any string. 
however if you try instead typing: 

{args}

Now run your command and type some extra words after it. cool huh.

- TODO - explain commands between bots / sharing commands
you can import pypals into other pypals and share commands between them.


### logging
- todo - explain logging. now off by default.

You can also call or execute any commands you created directly from the command line. i.e.

python3 -m pypals sportsfan hello


### meta / vars

At the root of every pypal you create is a _meta file to store variables.

If you don't like json you can change the config type (see below)

You can access any variables stored in _meta from your commands by using the passed in 'o' which is a reference to self.

print(f"Hello, to you { o.o['friend']}!")

You can store more variables in there if required just add them manually.


### shortcuts 

While a given pypal is running you can pass it the following single letter commands as shortcuts:

r - re-run previous command. (i.e. after editing the python file)

h - history

q - quit

c - list all the variables in the config file

c=json - change the config file to be json

c=ini - change the config file to be ini

c=xml - change the config file to be xml

c=txt - change the config file to be txt

d - generate a docs file inside the given pypals folder that list out all the commands you have created. (once you create a docs file for a pypal, it will auto update every time you create a new command. so don't edit it manually or you will lose your changes.)


## CLI

pypals has recently been updated to have a cli help system.

the following command might be useful...

for a list of all commands

	$ python3 -m pypals -h

the version of pypals you are using

	$ python3 -m pypals -v

show a list of all your pypals

	$ python3 -m pypals -l 

generate a top level docs file that lists out all your pypals in the root of the pypals folder.

	$ python3 -m pypals -d


### API

Every command gets passed a reference to self 'o' which is a reference to the pypals object.

There are some commands you can use on this object. But mostly you can use pypal to create your own

TODO - explain API


## documentation
- note : you can't use package names for commands. i.e. builtins, test
- note : use task manager to montior bots

the base path to a command is available if loading writing files to same folder:

o.context.COMMAND_PATH

pypals uses includes rich and domonic libraries so your commands should be able to import and use them.


## more
###  cron notes
put in sometask.sh file chmod +x the file.

	echo "do some job batch 1" | nohup python3 -m pypals jobs >/dev/null 2>&1 &

- you may want those to self terminate *see 'quit'


### makefile notes
something like this in your makefile to boot one or more faster

```
pypal:
	cd /home/ubuntu/Desktop/someapp/automate/; \
	python3 -m pypals myscraper somefunc
```

If you run several pypals simoultaneously you can trash them all easy by putting this in your makefile:

```
killall:
	pkill -9 python
```

## Notes
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56


## about
pypals was my first python project written in python2 in about 2012. It is a useful way to organise code snippets and do research. In 2019 I ported it to python 3 while learning to make pip packages.

please use it responsibly and if you want to contribute, fork it and send me a pull request.