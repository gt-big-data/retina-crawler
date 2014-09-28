This repo is in Python 2.7.8. You will need to 

1. [Install Python 2.7.8](https://www.python.org/download/releases/2.7.8/) and add Python to your path (if installing with `apt-get` or `brew` or an equivelant package manager on linux and mac systems, this should happen automatically
2. [Install pip](https://pip.pypa.io/en/latest/installing.html) the python package manager.
3. Optionally [install virtualenv](http://virtualenv.readthedocs.org/en/latest/) by running `pip install virtualenv`

Installation
============
To parse xml articles, you'll need two system packages, libxml2 and libxsl. On ubuntu, install with `sudo apt-get install libxml2 libxslt1-dev`

Then, install the required python libraries with:
`pip install -r requirements.txt`


Using Mongo
===========
1. [Install mongo](http://www.mongodb.org/downloads), then 
2. Install [genghisapp](http://genghisapp.com/) with `gem install genghisapp`, which is like PHPMyAdmin for MongoDB. genghisapp requires ruby / rubygems. You can install `ruby` by following [this guide](http://ruby.about.com/od/tutorials/a/installruby.htm) and install `gem` by [downloading and installing from here](https://rubygems.org/pages/download)

Running everything
==================
Once everything is installed, you should be able to run the crawler with
```
python main.py
```
