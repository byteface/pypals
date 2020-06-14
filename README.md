# pypals

Turns your python scripts/snippets into command line buddies

## install

	$ python3.7 -m pip insall pypals

## run

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

All clones live in /pypals directory. Pass their name to summon. i.e...

	$ python3 -m pypals sportsfan
	$ mike I see you have returned!
	$ I am listening...
	$ hello
	$ Hello, to you mike!
	$ I am listening...


- TODO - explain creating command with longer name. or just add that one that creates them.
- TODO - explain passing paramaters
- TODO - explain running headless
- TODO - the quit command

## MORE
- cron notes
- makefile notes

## DOCUMENTATION
note : you can't use package names for commands. i.e. builtins, test

- TODO - explain commands between bots / sharing commands
- TODO - provide more examples. i.e csv ingesters and webscrapers.

## SHORTCUTS 
r - repeats the last command
h - history

## LICENCE
http://www.gnu.org/licenses/gpl-3.0.html