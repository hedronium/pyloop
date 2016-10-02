import os,sys
import click
import json
from jsonschema import validate,ValidationError, SchemaError

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

					}
			},
			"author":self.author,
			"authorEmail": self.author_email
		}
		string = json.dumps(self.json,ensure_ascii=False,indent=4)
		self.json = string
		print(self.json)
		click.echo('This is will remove your previous pack.json and replace with new')
		sure = click.prompt('Are you sure you want renew/write your pack.json?', type=str, default='y')

		if (sure == 'y'):
			self.insertIntoFolder()
			self.installInitial()
		else:
			click.secho('Process aborted',fg='red')

	#Creates a new folder or replace with previous data
	def insertIntoFolder(self):
		file = open('pack.json','w')
		file.write(self.json)
		file.close()
		click.secho('Successfully created pack.json!',fg='green')

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
	def installer(self,commands):
		for command in commands:
			commandString = 'Running command "'+command+ '" ...'
			click.secho(commandString,fg='yellow')
			os.system(command)

	#installer script starts from here, extracting json data from pack.json
	def install(self,file):

		fopen = open(file)
		string = fopen.read()
		fopen.close()
		self.json = self.loadJson(string)
		self.validateSchema()
		self.getInstallInfo()
		
	#extract particuler information and call installer method
	def getInstallInfo(self):
		channels = self.json['channels']
		commands = []
		comString = ''
		channel = ''
		#print(channels)

		for key,value in channels.items():
			channel = key
			for key,value in channels[key].items():
				comString = channel + ' install ' + key + '=='+value
				commands.append(comString)
		#install everything in the list
		self.installer(commands)
		click.secho('Command executed sucessfully!',fg='green')

	def validateSchema(self):
		
		click.secho('validating json schema...',fg='blue')

		schema = {
			"type" : "object",
				"properties": {
					"name": {

							"type": "string"
						},
					
					"version": {
							"type":"string"
						},
					
					"author": {
							"type":"string"
						},
					
					"authorEmail":{
						
						"type":"string"
						
						},
					"description":{

						"type":"string"
						
						},
					"channels":{

							"type":"object",

							"properties": {

								"type":"string"

							}
					}

				}
		}

		try:
		
			validate(schema,self.json)
		
		except json.ValidationError as e:
			
			click.secho(e.message,fg='red')

		except json.SchemaError as e:

			click.secho(e,fg='red')

	# get data from cli command
	def get(self,count,file):
		commands = []

		pack_name = click.prompt('Package name', type=str)
		version   = click.prompt('Pacakge version',type=str)
		channel   = click.prompt('Package channel',type=str ,default='pip3')
		commandString = channel + ' install ' +  pack_name + '=='+version
		commands.append(commandString)
		click.secho('Checking for duplicate package under same channels....',fg='green')
		self.checkPackExists(file,pack_name,version,channel)


	#Loads json , it checks for json,and loads json string into self.json
	def loadJson(self,jsonString):
			
		if not jsonString:
			click.secho('pack.json is empty!',fg='red')
			exit()
		else:
			try:
				return json.loads(jsonString)
			except ValueError as e:
				click.secho(e,fg='red')
				exit()
	
	#check for pack exists and it will decide what will do
	def checkPackExists(self,file,pack_name,version,channel):

		commands = []
		match = ''

		fopen = open(file)
		string = fopen.read()
		fopen.close()
		self.json = self.loadJson(string)
		self.validateSchema()
		channels = self.json['channels']

		if channel not in channels:

			click.secho('New channel detected...',fg='green')
			self.add_channel(file,channel)
			self.addJson(file,pack_name,version,channel)

		else:

			for key,value in channels[channel].items():
				if (key == pack_name and value == version):
					match = 1
					break

				elif (key == pack_name and version != value):

					match = 2
					break

			if (match == 1):
				click.secho('ERROR: '+ pack_name + ' with a version of '+ version + ' is already in pack.json , it means ' + pack_name +  ' is already installed or run "pyloop install"',fg='red')
				exit()

			elif (match == 2):

				click.secho('WARNING: '+ pack_name + ' is already in the ' + channel + ' block , it will add the new version into pack.json',fg='yellow')
				check = click.prompt('Are you sure?', type=str,default='y')

				if (check == 'y'):
					commands.append(channel + ' install ' + key + '=='+value)
					#replace current version
					self.replaceJson(file,pack_name,version,channel)
				else:
					click.secho('Terminating current package installation process')					
			else:
				click.secho('Adding json data into pack.json...',fg='green')
				self.addJson(file,pack_name,version,channel)


	# Replace package version from a package name
	def replaceJson(self,file,pack_name,version,channel):
		
		channels = self.json['channels']
		channels[channel][pack_name] = version
		string = json.dumps(self.json,ensure_ascii=False,indent=4)

		os.system(channel +' install ' + pack_name + '==' + version)

		file = open(file,'w')
		file.write('')

		file.write(string)

		file.close()
		click.secho('Successfully updated new version pack.json , please run "pyloop update" to update packages',fg='green')


	#Adds data into a channel
	def addJson(self,file,pack_name,version,channel):
		channels = self.json['channels']
		channels[channel].update({ pack_name: version })
		string = json.dumps(self.json,ensure_ascii=False,indent=4)

		os.system(channel +' install ' + pack_name + '==' + version)

		file = open(file,'w')
		file.write('')

		file.write(string)

		file.close()
		click.secho('Successfully added ' + pack_name + ' with version '+ version +' in pack.json into ' + channel + ' channel, please run "pyloop update" to update packages',fg='green')

	# adds extra channel into channels
	def add_channel(self,file,channel):
		channels = self.json['channels']
		data = { channel: {} }
		channels.update(data)
		string = json.dumps(self.json,ensure_ascii=False,indent=4)

		file = open(file,'w')
		file.write('')

		file.write(string)

		file.close()
		click.secho('Successfully added a new channel name "' + channel + '"...',fg='green')
