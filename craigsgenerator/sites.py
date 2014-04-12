try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

import requests
import lxml.html
from pickle_warehouse import Warehouse

from craigsgenerator.download import download

def sites(get = requests.get, url = 'http://www.craigslist.org/about/sites', cachedir = 'sites'):
    '''
    Generate craigslist sites.
    '''
    warehouse = Warehouse(cachedir)

    response = download(get, warehouse, url, None)
    html = lxml.html.fromstring(response.text)

    return set(filter(None, (urlsplit(href).netloc for href in html.xpath('//a/@href'))))
