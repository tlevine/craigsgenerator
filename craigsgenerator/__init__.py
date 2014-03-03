import re
import os
import urllib.parse
import datetime

import lxml.html
from pickle_warehouse import Warehouse

import craigsgenerator.download as download
import craigsgenerator.parse as parse

def section(subdomain, section, cachedir = 'craigslist', scheme = 'https', get = requests.get, date_func = datetime.date):
    try:
        results = []
        html = None
        warehouse = Warehouse(cachedir)
        while True:
            for result in results:
                href = result.get('href')
                if href is not None:
                    response = download(get, warehouse, href, date_func()):
                    html = parse.load_response(response)
                    # result.update(parse.???(html))
                    yield result

            url = parse.next_search_url(scheme, subdomain, section, html)
            if url is None:
                break

            response = download.download(get, warehouse, url, date_func())
            html = parse.load_response(response)
            results.extend(parse.search(html))
            if results == []:
                break
    except GeneratorExit:
        pass

def subdomains(get = requests.get, url = 'https://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar', date_func = datetime.date):
    '''
    Generate craigslist subdomains.
    '''
    results = set()
    warehouse = Warehouse(cachedir)

    response = parse.download(get, warehouse, url, date_func)
    html = parse.load_response(response)

    for href in html.xpath('id("%s")/descendant::a/@href' % id):
        p = urllib.parse.urlparse(href.rstrip('/'))
        if p.fragment:
            pass
        elif p.path:
            results.update(subdomains(get = requests.get, url = href, cachedir = cachedir, id = 'list', date_func = date_func))
        elif p.netloc not in results:
            results.add(p.netloc)
            yield p.netloc
