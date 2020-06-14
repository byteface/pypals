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

## installation

	Get the package from PyPI i.e.

	$ python3.7 -m pip install pypals

## usage

Sometimes you write code maybe to do some random job or snippet, scrape something, send a tweet, whatever.

It's good to keep those bits of odd code somewhere. pypals are good and easy to remember ages later.


	$ python3 -m pypals sportsfan
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

Next try typing a command like 'scrape somesite.com for images'...

- TODO - explain creating command with longer name. or just add that one that creates them.
- TODO - explain passing paramaters
- TODO - explain running headless
- TODO - the quit command

## MORE
- cron notes

echo "do some job batch 1" | nohup python3.7 -m pypals jobs >/dev/null 2>&1 &

echo "do some job batch 2" | nohup python3.7 -m pypals jobs >/dev/null 2>&1 &

- makefile notes

pypal:

	cd /home/ubuntu/Desktop/someapp/automate/; \

	python3.7 -m pypals myscraper server.py



If you run several pypals simoultaneously you can trash them all easy by putting this in your makefile:

killall:
	sudo service solr stop; \
	pkill -9 python


## DOCUMENTATION
note : you can't use package names for commands. i.e. builtins, test

- TODO - explain commands between bots / sharing commands
- TODO - provide more examples. i.e csv ingesters and webscrapers.
- TODO - using task manager to montior bots?

## SHORTCUTS 
r - re-run previous command

h - history

## Notes
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56