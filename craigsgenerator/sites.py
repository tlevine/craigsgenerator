try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

import requests
import lxml.html
from pickle_warehouse import Warehouse

from craigsgenerator.download import download

def sites(get = requests.get, url = 'http://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar'):
    '''
    Generate craigslist sites.
    '''
    results = set()
    warehouse = Warehouse(cachedir)

    response = download(get, warehouse, url, None)
    html = lxml.html.fromstring(response.text)

    for href in html.xpath('id("%s")/descendant::a/@href' % id):
        p = urlsplit(href.rstrip('/'))
        if p.fragment:
            pass
        elif p.path:
            for netloc in sites(get = requests.get, url = href, cachedir = cachedir, id = 'list'):
                results.add(netloc)
                yield netloc
        elif p.netloc not in results:
            results.add(p.netloc)
            yield p.netloc
