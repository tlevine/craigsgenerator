import re
import os
import urllib.parse
import datetime

import lxml.html
from pickle_warehouse import Warehouse

import craigsgenerator.download as download
import craigsgenerator.parse as parse

#logger = Logger('craigsgenerator')

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

def subdomains(url = 'https://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar'):
    results = set()
    with open(get(cachedir, url, False)) as fp:
        html = lxml.html.fromstring(fp.read())

    for href in html.xpath('id("%s")/descendant::a/@href' % id):
        p = urllib.parse.urlparse(href.rstrip('/'))
        if p.fragment:
            pass
        elif p.path:
            results.update(subdomains(url = href, cachedir = cachedir, id = 'list'))
        else:
            results.add(p.netloc)
    return results

def bump_url(scheme, subdomain, section, html):
    url = next_search_url(scheme, subdomain, section, html)
    if url is None:
        raise ValueError('No next page')
    return url
