import click
import os
import sys
from termcolor import cprint
from pyfiglet import figlet_format
from .process import Process

process = Process()
cprint(figlet_format('Pyloop!', font='starwars'), 'green', attrs=['bold'])


@click.group()
def index():
    pass


@index.command('install')
def install():
    """ installs everything in the pack.json file """
    file = os.getcwd() + '/pack.json'
    process.install(file)


@index.command('init')
def init():
    """ initialize json file """
    click.secho("Initializing json file as pack.json", fg='green')
    file_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

    name = click.prompt('Name', type=str, default=file_name)
    version = click.prompt('Version', type=str, default='1.0.0')
    description = click.prompt('Description', type=str, default='')
    author = click.prompt('Author Name', type=str, default='')
    author_email = click.prompt('Author Email', type=str, default='')
    channels = click.prompt('Channels (comma separated)', type=str, default="pip,pip3")

    # inserting data into class variables
    process.get_cli_data(name, version, description, author, author_email, channels)


@index.command('get')
@click.option('--count', default=1, help='How many packages do you want to install?')
def get(count):
    """ get desired packages installed """
    file = os.getcwd() + '/pack.json'
    process.get(count, file)


@index.command('clear')
def clear():
    """ clear screens """
    click.clear()
