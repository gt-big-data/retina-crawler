# Crawler Config Format
All Crawler config files are json files with two root values:

* crawler: The name of the Python class to use as a crawler. The recommended class to use is `ModularCrawler`.
* args: A dictionary of arguments to pass to the given crawler.


## Modular Crawler Format
The following parameters are accepted by the `ModularCrawler`:

* threads: A string representing the number of threads to use while downloading and processing articles. A value of 1 will use single-threaded code. A value greater than 1 will use multiple processes. A value of 0 will use the number of threads that the current computer has.
* output: Determines how the processed articles should be outputted. Supported values are `file`, `mongo`, and `print`. `print` will print everything to the console.
* urls: A list of article URLS to crawl. These must be actual articles (vs. RSS feeds).
* feeds: A list of RSS feeds to grab articles from. These URLS must be actual RSS feeds (vs. article URLS).
