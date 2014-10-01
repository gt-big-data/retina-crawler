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
python poc.py
```

This will run the crawler in "SimpleMode," which will crawl articles from the CNN RSS feed, and write them to a directory as JSON files.

To configure different behavior, you can pass the path to a configuration file (in json format) as the first command line argument. For example, to run on several RSS feeds and storing results to mongo db running on localhost, you can run the following command
```
python poc.py configs/local-mongo-several-rss-conf.json
```

Format of configs
=================
[See this as an example](https://github.com/gt-big-data/retina-crawler/blob/master/configs/local-mongo-several-rss-conf.json).

You can make new configs and runners in the following way. First, in the file `CrawlerRunners.py` add a class with a `run` method. `run` will run in a `while (true)` loop, and any errors thrown will be caught by external code and logged.

Example:
Suppose we made the following runner in `CrawlerRunners.py`, which will simply print new links from an RSS feed:

```
class RSSLinkPrinter(object):
    def __init__(self, args):
        self._rssRunner = RssLinkParser(args['rss_feed')
    
    def run(self):
        print self._rssRunner.get_new_links()
```

Which RSS feed will this pull from? Let's say we want to test out the New York Times RSS feed. Then we should make the following configuration file, 'print-nytimes-rss-links.json'
```
{
  "runner" : "RSSLinkPrinter",
  "args" : {
    "rss_feed" : "http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"
  }
}
```

The `"runner"` field in the JSON file is the name of the class you defined in `CrawlerRunners.py`, and the `args` field is a dict that will be passed directly to the constructor of your runner.
