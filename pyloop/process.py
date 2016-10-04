import os, sys
import click
import json
from jsonschema import validate, ValidationError, SchemaError


class Process:
    def __init__(self):

        self.name = ''
        self.version = ''
        self.description = ''
        self.author = ''
        self.author_email = ''
        self.channels = ''
        self.json = ''

    # Receive cli data from terminal
    def get_cli_data(self, name, version, description, author, author_email, channels):

        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.author_email = author_email

        self.channels = channels.split(',')
        total_comma = channels.count(',')

        if (len(self.channels) - 1) == total_comma:
            self.create_json()
        else:
            click.secho('The channels should be a comma separated string', fg='red')

    # Creates json schema
    def create_json(self):
        self.json = {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "channels": {

                "pip": {

                },
                "pip3": {

                }
            },
            "author": self.author,
            "authorEmail": self.author_email
        }
        string = json.dumps(self.json, ensure_ascii=False, indent=4)
        self.json = string
        print(self.json)
        click.echo('This will remove your previous pack.json file and replace with new one.')
        sure = click.prompt('Are you sure you want to renew/write to your pack.json file?', type=str, default='y')

        if sure == 'y':
            self.insert_into_folder()
        else:
            click.secho('Process aborted', fg='red')

    # Creates a new folder or replace with previous data
    def insert_into_folder(self):
        file = open('pack.json', 'w')
        file.write(self.json)
        file.close()
        click.secho('Successfully created pack.json!', fg='green')

    # it's job is to install everything
    def installer(self, commands):
        for command in commands:
            command_string = 'Running command "' + command + '" ...'
            click.secho(command_string, fg='yellow')
            os.system(command)

    # installer script starts from here, extracting json data from pack.json
    def install(self, file):
        fopen = open(file)
        string = fopen.read()
        fopen.close()
        self.json = self.load_json(string)
        self.validate_schema()
        self.get_install_info()

    # extract particular information and call installer method
    def get_install_info(self):
        channels = self.json['channels']
        commands = []
        com_string = ''
        channel = ''
        # print(channels)

        for key, value in channels.items():
            channel = key
            for key, value in channels[key].items():
                com_string = channel + ' install ' + key + '==' + value
                commands.append(com_string)
        # install everything in the list
        self.installer(commands)
        click.secho('Command executed successfully!', fg='green')

    def validate_schema(self):
        click.secho('Validating json schema...', fg='blue')

        schema = {
            "type": "object",
            "properties": {
                "name": {

                    "type": "string"
                },

                "version": {
                    "type": "string"
                },

                "author": {
                    "type": "string"
                },

                "authorEmail": {

                    "type": "string"

                },
                "description": {

                    "type": "string"

                },
                "channels": {

                    "type": "object",

                    "properties": {

                        "type": "string"

                    }
                }

            }
        }

        try:
            validate(schema, self.json)
        except json.ValidationError as e:
            click.secho(e.message, fg='red')
        except json.SchemaError as e:
            click.secho(e, fg='red')

    # get data from cli command
    def get(self, count, file):
        commands = []

        pack_name = click.prompt('Package name', type=str)
        version = click.prompt('Package version', type=str)
        channel = click.prompt('Package channels', type=str, default='pip3')
        command_string = channel + ' install ' + pack_name + '==' + version
        commands.append(command_string)
        click.secho('Checking for duplicates package under same channels...', fg='green')
        self.check_pack_exists(file, pack_name, version, channel)

    # Loads json, it checks for json, and loads json string into self.json
    def load_json(self, json_string):

        if not json_string:
            click.secho('pack.json is empty!', fg='red')
            exit()
        else:
            try:
                return json.loads(json_string)
            except ValueError as e:
                click.secho(e, fg='red')
                exit()

    # check for pack exists and it will decide what will do
    def check_pack_exists(self, file, pack_name, version, channel):

        commands = []
        match = ''

        fopen = open(file)
        string = fopen.read()
        fopen.close()
        self.json = self.load_json(string)
        self.validate_schema()
        channels = self.json['channels']

        if channel not in channels:
            click.secho('New channel detected...', fg='green')
            self.add_channel(file, channel)
            self.add_json(file, pack_name, version, channel)
        else:
            for key, value in channels[channel].items():
                if key == pack_name and value == version:
                    match = 1
                    break

                elif key == pack_name and version != value:
                    match = 2
                    break

            if match == 1:
                click.secho(
                    'ERROR: ' + pack_name + ' with a version of ' + version + ' already exists in pack.json , it means ' + pack_name + ' is already installed or run "pyloop install"',
                    fg='red')
                exit()
            elif match == 2:
                click.secho(
                    'WARNING: ' + pack_name + ' already exists in the ' + channel + ' block, It will add the new version into pack.json',
                    fg='yellow')
                check = click.prompt('Are you sure?', type=str, default='y')

                if check == 'y':
                    commands.append(channel + ' install ' + key + '==' + value)
                    # replace current version
                    self.replace_json(file, pack_name, version, channel)
                else:
                    click.secho('Terminating current package installation process!')
            else:
                click.secho('Adding json data into pack.json...', fg='green')
                self.add_json(file, pack_name, version, channel)

    # Replace package version from a package name
    def replace_json(self, file, pack_name, version, channel):

        channels = self.json['channels']
        channels[channel][pack_name] = version
        string = json.dumps(self.json, ensure_ascii=False, indent=4)

        os.system(channel + ' install ' + pack_name + '==' + version)

        file = open(file, 'w')
        file.write('')

        file.write(string)

        file.close()
        click.secho('Successfully updated new version pack.json, please run "pyloop update" to update packages',
                    fg='green')

    # Adds data into a channel
    def add_json(self, file, pack_name, version, channel):
        channels = self.json['channels']
        channels[channel].update({pack_name: version})
        string = json.dumps(self.json, ensure_ascii=False, indent=4)

        os.system(channel + ' install ' + pack_name + '==' + version)

        file = open(file, 'w')
        file.write('')

        file.write(string)

        file.close()
        click.secho(
            'Successfully added ' + pack_name + ' with version ' + version + ' in pack.json into ' + channel + ' channel, Please run "pyloop update" to update packages',
            fg='green')

    # adds extra channel into channels
    def add_channel(self, file, channel):
        channels = self.json['channels']
        data = {channel: {}}
        channels.update(data)
        string = json.dumps(self.json, ensure_ascii=False, indent=4)

        file = open(file, 'w')
        file.write('')

        file.write(string)

        file.close()
        click.secho('Successfully added a new channel named "' + channel + '"...', fg='green')
