from distutils.core import setup

setup(
		name="pyloop",
		version="0.14",
		py_modules = ['pyloop.app'],
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
		download_url = 'https://github.com/Hedronium/pyloop/tarball/0.13',
		author = 'Hedronium',
		keywords = ['package manger','python 3'],
		author_email= 'project.anik@gmail.com',
		licence='MIT'
	)