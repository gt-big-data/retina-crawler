# Crawler Config Format
All Crawler config files are json files with two root values:

* `crawler`: The name of the Python class to use as a crawler. The recommended class to use is `ModularCrawler`.
* `args`: A dictionary of arguments to pass to the given crawler.


## Modular Crawler Format
The following parameters are accepted by the `ModularCrawler`:

* `threads`: A string representing the number of threads to use while downloading and processing articles. A value of 1 will use single-threaded code. A value greater than 1 will use multiple processes. A value of 0 will use the number of threads that the current computer has.
* `output`: Determines how the processed articles should be outputted. Supported values are `file`, `mongo`, and `print`. `print` will print everything to the console.
* `urls`: A list of article URLS to crawl. These must be actual articles (vs. RSS feeds).
* `feeds`: A list of RSS feeds to grab articles from. These URLS must be actual RSS feeds (vs. article URLS).

## Creating New Crawlers
Creating a new crawler is easy. First, add a new class in [`crawlers.py`](../crawlers.py) and make sure it has an `__init__` that takes an `args` parameter. `args` is supposed to be a dictionary of arguments (but you should still check to make sure that it is).

Your new class also needs a `run` method that takes no parameters. It will be called in a `while (true)` loop that will catch and log any errors that happen to get thrown. Ideally, the `run` method should gracefully handle as many exceptions as it can before it allows one to bubble up to the main loop.

Example:
Suppose we made the following crawler in `crawlers.py`, which will simply print new links from an RSS feed:

```
class RSSLinkPrinter(object):
    def __init__(self, args):
        self._rssRunner = RssLinkParser(args['rss_feed'])
    
    def run(self):
        print self._rssRunner.get_new_links()
```

*Note:* The above example does not do any exception handling. A good, robust crawler should.

Which RSS feed will this pull from? Let's say we want to test out the New York Times RSS feed. Then we should make the following configuration file, `print-nytimes-rss-links.json`
```
{
  "crawler" : "RSSLinkPrinter",
  "args" : {
    "rss_feed" : "http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"
  }
}
```

The `"crawler"` field in the JSON file is the name of the class you defined in `crawlers.py`, and the `args` field is a dict that will be passed directly to the constructor of your crawler.

Now we can run the crawler with our RSSLinkPrinter with the following command:
```
python main.py print-nytimes-rss-links.json
```

*Note:* To keep things organized, please put all permanent configuration files in the `configs/` directory.