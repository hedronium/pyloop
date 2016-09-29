import os,sys
import click
import json

class process:
	def __init__(self):

		self.name = ''
		self.version = ''
		self.description = ''
		self.author = ''
		self.author_email = ''
		self.channels = ''
		self.json = ''

	#Recive cli data from terminal
	def getCliData(self,name,version,description,author,author_email,channels):

		self.name = name
		self.version = version
		self.description = description
		self.author = author
		self.author_email = author_email

		self.channels = channels.split(',')
		totalcomma  = channels.count(',')

		if ((len(self.channels)-1) == totalcomma ):
			self.createJson()
		else:
			click.secho('The channels should be a comma separeted string',fg='red')

	#Creates json schema from 
	def createJson(self):
		self.json = {
			"name": self.name,
			"version": self.version,
			"description": self.description,
			"channels": {

					"pypi":{

					},
					"pip":{

					},
					"pip3":{

					},
					"pypm":{

					}
			},
			"author":self.author,
			"authorEmail": self.author_email
		}
		string = json.dumps(self.json,ensure_ascii=False,indent=4)
		self.json = string
		print(self.json)
		click.echo('This is will remove your previous pack.json and replace with new')
		sure = click.prompt('Are you sure you want renew your pack.json?', type=str, default='y')

		if (sure == 'y'):
			self.insertIntoFolder()
		else:
			click.secho('Process aborted',fg='red')

	#Creates a new folder or replace with previous data
	def insertIntoFolder(self):
		file = open('pack.json','w')
		file.write(self.json)
		file.close()

	#installing intital file
	def installInitial(self):
		click.secho('To make things more comfortable we want to install some packages(pip,pip3,pypi,pypm)',fg='yellow')
		sure = click.prompt('Will you allow to install?',default='y',type=str)
		if (sure == 'y'):
			commands = [
				'python install pip',
				'python3 install pip3',
				'python3 install pypi',
				'python3 install pypm'
			]
			self.installer(commands)
		else:
			click.secho("process aborted",fg='red')

	#it's job is to install everythin
	def installer(commands):
		for command in commands:
			commandString = 'Running command '+command
			click.secho(command,fg='yellow')
			sys.command(command)