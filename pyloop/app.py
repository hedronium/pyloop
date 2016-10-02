import click
import os
import sys
from termcolor import cprint 
from pyfiglet import figlet_format
from .process import process

process = process()
cprint(figlet_format('Pyloop!', font='starwars'),'green', attrs=['bold'])

@click.group()
def index():
	pass

@index.command('install')
def install():
	""" Installs everything in the pack.json	 """
	file = os.getcwd()+'/pack.json'
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
	channels 		= click.prompt('Channels(comma separated)',type=str,default="pip,pip3")

	#inserting data into class variables
	process.getCliData(name,version,description,author,author_email,channels)



@index.command('get')
@click.option('--count',default=1,help='How many packages you want to install')
def get(count):
	""" get desired package installed """
	file = os.getcwd()+'/pack.json'
	process.get(count,file)

@index.command('clear')
def clear():
	""" Clear screens """
	click.clear()