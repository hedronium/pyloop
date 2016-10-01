from setuptools import setup

setup(
		name="Pyloop",
		version="0.10",
		py_modules = ['app'],
		install_requires=[
			'Click',
			'colorama',
			'termcolor',
			'pyfiglet',
			'jsonschema'
		],
		entry_points = '''
			[console_scripts]
			pyloop=app:index
		''',
		author = 'Hedronium',
		author_email= 'aniruddha@anichakraborty.me'
	)