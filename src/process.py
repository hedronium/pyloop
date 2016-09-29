import click

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
		print(totalcomma)
		if (self.channels == (totalcomma - 1)):
			self.createJson()
		else:
			click.secho('The channels should be a comma separeted string',fg='red')

	#Creates json schema from 
	def createJson():
		self.json = {

			"name": self.name,
			"version": self.version,
			"description": self.description
		}
		print(self.channels.json())