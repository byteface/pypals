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
Get the package from PyPI i.e.

	$ python3.7 -m pip install pypals

## usage
Sometimes you write code maybe to do some random job or snippet, scrape something, send a tweet, whatever.

It's useful to keep those bits of odd code somewhere. pypals are easy to remember ages later.

	$ python3.7 -m pypals sportsfan
	$ sportsfan doesn't exist, create them now? yes or no
	$ > yes
	$ your name?
	$ > mike
	$ Hi my name is sportsfan, Thankyou for creating me!
	$ I am listening...

sportsfan has been created, you can see him in /pypals directory. He can gather data about sports using any python commands you write and put in that folder

now try running this command...

	$ hello

look in pypals/sportsfan/hello/hello.py file to see an example of a command. Add as many commands as you like for your project.

Next try typing a command like 'scrape somesite for images'...

You see it creates it for you. you can then just fill it in.

Next try typing 'quit'

If you're editing a python command you don't need to restart pypal. It will reload the command. so just type 'r' to rerun it.

- TODO - explain passing paramaters
- TODO - explain commands between bots / sharing commands


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
	python3.7 -m pypals myscraper server.py
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
- r - re-run previous command
- h - history

## Notes
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56