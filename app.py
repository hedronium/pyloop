import click
import os
#from app import inits
import sys
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format
cprint(figlet_format('Pyloop!', font='starwars'),
       'green', attrs=['bold'])

@click.group()
def index():

	pass

@index.command('install')
def install(string):
	""" Scripts that greets you """
	print(string)


@index.command('init')
def init():
	""" Initialize json file """ 
	file_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
	
	name 			= click.prompt('name', type=str) | file_name
	version 		= click.prompt('version',type=str) | '1.0.0'
	description 	= click.prompt('description',type=str)
	author 			= click.prompt('author',type=str)
	author_email 	= click.prompt('author email',type=str)
	channels 		= click.prompt('Channels(comma separated)',type=str) | ['pip','pip3','pypy']

@index.command('update')
def update():
	""" Updates from json folder """
	return 0

@index.command('clear')
def clear():
	""" Clear screens """
	click.clear()