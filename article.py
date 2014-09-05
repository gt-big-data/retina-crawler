import newspaper
from newspaper import news_pool

import json
try:
    import cPickle as pickle
except:
    import pickle

def create_article(article_url):
    article = newspaper.build_article(article_url)
    article.download()
    article.parse()
    return article

# def create_articles(article_urls):


def article_dictionary(article):
    if (not article.is_downloaded):
        article.download()

    if (not article.is_parsed):
        article.parse()

    dict = {}
    dict['title'] = article.title
    dict['authors'] = article.authors
    dict['url'] = article.url
    dict['canonical_link'] = article.canonical_link
    dict['images'] = article.images
    dict['article_html'] = article.article_html
    dict['additional.additional_data'] = article.additional_data
    dict['keywords'] = article.keywords
    dict['imgs'] = article.imgs
    dict['text'] = article.text
    dict['meta_data'] = article.meta_data
    dict['html'] = article.html
    dict['meta_description'] = article.meta_description
    dict['meta_keywords'] = article.meta_keywords
    dict['meta_lang'] = article.meta_lang
    dict['meta_img'] = article.meta_img
    return dict

def dump_article_to_json(article, filename):
    article_dict = article_dictionary(article)
    with open(filename, 'w') as file:
        json.dump(article_dict, file)
