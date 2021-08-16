<h1 align="center">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTe1LJtuvY4cuG7yN2ib3IYmFRU7nayGL3cDYSS8ckTrykpnRgJ&usqp=CAU"
    style="background-color:rgba(0,0,0,0);" height=230 alt="pypals: it really does nothing!">
    <br>
    pypals
    <br>
    <sup><sub><sup>Turn python snippets into command line buddies!</sup></sub></sup>
    <br>
</h1>

Keeps track of python scripts and snippets as command line pals.

[![PyPI version](https://badge.fury.io/py/pypals.svg)](https://badge.fury.io/py/pypals.svg)

[![Downloads](https://pepy.tech/badge/pypals)](https://pepy.tech/project/pypals)

## installation
Get the package from pypi i.e.

	$ python3 -m pip install pypals

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

now look in pypals/sportsfan/hello/hello.py file to see an example of a command. Add as many commands as you like for your project.

To create commands try typing 'scrape somesite for images' at the prompt.

You will see it creates it for you. You can now just edit the file created and fill it.

Next try typing 'quit'

If you're editing a python command you don't need to restart pypal. It will reload the command. so just type 'r' to rerun it at the prompt.

- TODO - explain passing paramaters
- TODO - explain commands between bots / sharing commands


## help

pypals has recently been updated to have a cli help system.

the following command might be useful...

--help
	$ python3 -m pypals -h

a list of all commands

--version
	$ python3 -m pypals -v

the version of pypals you are using.

--list
	$ python3 -m pypals -l 

shows a list of all your pypals


## more
###  cron notes
put in sometask.sh file chmod +x the file.

	echo "do some job batch 1" | nohup python3.7 -m pypals jobs >/dev/null 2>&1 &

- you may want those to self terminate *see 'quit'

### makefile notes
something like this in your makefile to boot one or more faster

```
pypal:
	cd /home/ubuntu/Desktop/someapp/automate/; \
	python3 -m pypals myscraper server.py
```

If you run several pypals simoultaneously you can trash them all easy by putting this in your makefile:

```
killall:
	pkill -9 python
```

## documentation
- note : you can't use package names for commands. i.e. builtins, test
- note : use task manager to montior bots

the base path to a command is available if loading writing files to same folder:

o.context.COMMAND_PATH

### shortcuts 

while a pypal is running you can pass it the following commands as shortcuts

- r - re-run previous command. (i.e. after editing the python file)
- h - history

## Notes
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56


## about
pypals was my first every python project written in python2 in about 2012. It is a useful way to organise code snippets and do research. In 2019 I ported it to python 3 while learning to make pip packages.
