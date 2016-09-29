from setuptools import setup

setup(
		name="Pyloop",
		version="0.01",
		py_modules = ['app'],
		install_requires=[
			'Click',
			'colorama',
			'termcolor',
			'pyfiglet'
		],
		entry_points = '''
			[console_scripts]
			pyloop=app:index
		''',
		author = 'Hedronium',
		author_email= 'aniruddha@anichakraborty.me'
	)