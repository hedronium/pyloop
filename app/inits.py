class inits:
	def __init__(self):
	self.name = ''
	self.version = ''
	self.description = ''
	self.author = ''
	self.author_email = ''
	self.repositories = []


	def getCliData(self,name,version,description,author,author_email,repositories):
		self.name = name
		self.version = version
		self.description = description
		self.author = author
		self.author_email = author_email

		