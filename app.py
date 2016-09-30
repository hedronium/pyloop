import click
import os
#from app import inits
import sys
from termcolor import cprint 
from pyfiglet import figlet_format
from src.process import process

process = process()
cprint(figlet_format('Pyloop!', font='starwars'),'green', attrs=['bold'])

@click.group()
def index():
	pass

@index.command('install')
def install():
	""" Scripts that greets you """
	file = os.getcwd()+'/pack.json'
	print(file)
	process.install(file)


@index.command('init')
def init():
	""" Initialize json file """
	click.secho("Intializing json file as pack.json",fg='green')
	file_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

	name 			= click.prompt('name', type=str, default=file_name)
	version 		= click.prompt('version',type=str,default='1.0.0')
	description 	= click.prompt('description',type=str,default='')
	author 			= click.prompt('author',type=str,default='')
	author_email 	= click.prompt('author email',type=str,default='')
	channels 		= click.prompt('Channels(comma separated)',type=str,default="pip,pip3,pypy")

	#inserting data into class variables
	process.getCliData(name,version,description,author,author_email,channels)


@index.command('update')
def update():
	""" Updates from json folder """
	return 0

@index.command('clear')
def clear():
	""" Clear screens """
	click.clear()