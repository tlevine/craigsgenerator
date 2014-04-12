import lxml.html
from craigsgenerator.download import download

def _sections(get, warehouse, url):
    response = download(get, warehouse, url, None)
    html = lxml.html.fromstring(response.text)
    all = list(map(str, html.xpath('id("main")/descendant::a/@href')))
    simple = list(href.rstrip('/') for href in all if len(href) == 4)
    complicated = list(filter(lambda href: len(href) != 4 and href.startswith('/i/'), all))
    return simple, complicated

import requests
from pickle_warehouse import Warehouse
def sections(get = requests.get, warehouse = Warehouse('sections'),
             url = 'http://sfbay.craigslist.org'):
    return _sections(get, warehouse, url)
