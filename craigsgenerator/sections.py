import warnings

import lxml.html
from craigsgenerator.download import download

def _sections(get, warehouse, url):
    response = download(get, warehouse, url, None)
    html = lxml.html.fromstring(response.text)
    for href in map(str, html.xpath('id("main")/descendant::a/@href')):
        if len(href) == 4:
            yield href.rstrip('/')
        elif href.startswith('/i/personals/'):
            yield href.replace('/i/personals?category=','')
        elif href.startswith('/i/'):
            warnings.warn('Go to %s to see more sections.' % href)

import requests
from pickle_warehouse import Warehouse
def sections(get = requests.get, warehouse = Warehouse('sections'),
             url = 'http://sfbay.craigslist.org'):
    return _sections(get, warehouse, url)
