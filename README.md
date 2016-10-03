# Pyloop
An universal npm like package manager for python
## How it works?
> it uses json data to track your installed packages using channels like pip or pypy . pyloop will help programmers to maintain multiple package installation using multiple channels.

## Installation
> Grab it using pip

```bash
sudo pip3 install pyloop
```

# Usage #

### intialize pyloop
```bash
pyloop init
```
It will create a pack.json file into the project directory

### write 
```json
{
    "authorEmail": "",
    "author": "",
    "description": "",
    "name": "pyloop",
    "version": "1.0.0",
    "channels": {
       "pip3": {
            "flask": "0.7" ,
            "flask-WTF": "0.9"
        },
        "pip": {
            
            "django": "1.9",
        }
    }
}
```

### install packages (from pack.json)
it will install all your packages globally (because pip or pypy install everything globally)
```bash
sudo pyloop install
```

### update packages
it will update all your packages globally (because pip or pypy install everything globally)

```bash
sudo pyloop update
```

### install packages using pyloop (It'll update pack.json)

```bash
sudo pyloop get
```
