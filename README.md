This repo is in Python 2.7.8. You will need to 

1. [Install Python 2.7.8](https://www.python.org/download/releases/2.7.8/) and add Python to your path (if installing with `apt-get` or `brew` or an equivelant package manager on linux and mac systems, this should happen automatically
2. [Install pip](https://pip.pypa.io/en/latest/installing.html) the python package manager.
3. Optionally [install virtualenv](http://virtualenv.readthedocs.org/en/latest/) by running `pip install virtualenv`

Installation
============
To parse xml articles, you'll need two system packages, libxml2 and libxsl. On ubuntu, install with `sudo apt-get install libxml2 libxslt1-dev`

Then, install the required python libraries with:
`pip install -r requirements.txt`

**Windows Note:** Running the above command will only partially work and will error on libxml. You must manually [download and install it](https://pypi.python.org/pypi/lxml).

Using Mongo
===========
1. [Install mongo](http://www.mongodb.org/downloads)
2. Install [genghisapp](http://genghisapp.com/) with `gem install genghisapp`, which is like PHPMyAdmin for MongoDB. genghisapp requires ruby / rubygems. You can install `ruby` by following [this guide](http://ruby.about.com/od/tutorials/a/installruby.htm) and install `gem` by [downloading and installing from here](https://rubygems.org/pages/download)

Running everything
==================
Once everything is installed, you can run the crawler with
```
python main.py configs/simple-config.json
```

This will run the crawler with the simplest possible setup. It will crawl articles from the main CNN RSS feed and write them to a directory as JSON files.

To configure different behavior, you can specify a different configuration file. There are several pre-built configuration files in the [`configs/`](configs/) directory. If none of them do what you want, consider making a new configuration. See [`configs/configuration.md`](configs/configuration.md) for more details.

# Running with Vagrant
- [Install Vagrant](https://www.vagrantup.com/downloads.html)
- Start and provision Vagrant environment with `vagrant up`
- Enter Vagrant environment with `vagrant ssh`

The project directory is by default mapped to /vagrant in the virtual machine.
