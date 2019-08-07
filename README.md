#pypals

ported up my first ever python project from several years back from python2 to python3

command line python friends for storing and running python code scripts and snippets

	$ python3 run.py sportsfan
	$ sportsfan doesn't exist, create them now? yes or no
	$ > yes
	$ your name?
	$ > mike
	$ Hi my name is sportsfan, Thankyou for creating me!
	$ I am listening...

sportsfan has been created, you can see him in /bin directory. He can gather data about sports using any python commands you write and put in the commands folder

now try running this command...

	$ hello

look in bin/skeleton/brain/commands/hello/hello.py file to see an example of a command. clones have brains that store 'commands' to consume and process data, do tasks or whatever. Add as many commands as required for your project. If you come back ages later to a project, it's easy to remember how it works and what they do. As they are just plain english commands.

All clones live in the /bin . pass their name to summon. i.e...

	$ python3 run.py sportsfan
	$ mike I see you have returned!
	$ I am listening...
	$ hello
	$ Hello, to you mike!
	$ I am listening...

now try running this command...

	$ quit

Clones of are copies of '/bin/skeleton' which is empty as possible to keep any new pypals you make light. But you could change code to set your own base to clone from.

I create them mostly for scraping data or organising and running tasks on projects. i.e you could have several pypals in the bin...

bin/somesite
bin/someapp
bin/somesideproject
bin/somewebscraper

with commands for doing various tasks. I have many and you can eventually build up libraries and share or call commands between pypals.

##MORE
You can install loads of python libraries and do tons of stuff with them. this is just the empty loader.


##DOCUMENTATION
cant use package names for commands. i.e. builtins

##SHORTCUTS
r - repeats the last command
h - history


##LICENCE
http://www.gnu.org/licenses/gpl-3.0.html