from setuptools import setup

setup(
		name="pyloop",
		version="0.12",
		py_modules = ['app'],
		packages = ['pyloop'],
		description='An universal pacakge manager for python',
		install_requires=[
			'Click',
			'colorama',
			'termcolor',
			'pyfiglet',
			'jsonschema'
		],
		entry_points = '''
			[console_scripts]
			pyloop=pyloop.app:index
		''',
		url='https://github.com/Hedronium/pyloop',
		download_url = 'https://github.com/Hedronium/pyloop/tarball/0.12',
		author = 'Hedronium',
		keywords = ['package manger','python 3'],
		author_email= 'project.anik@gmail.com',
		licence='MIT'
	)