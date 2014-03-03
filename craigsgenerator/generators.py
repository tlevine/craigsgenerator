import re
import os
import urllib.parse
import datetime

import lxml.html
from pickle_warehouse import Warehouse

import craigsgenerator.download as download
import craigsgenerator.parse as parse

def listings(site, section, cachedir = 'craigslist', scheme = 'https', get = requests.get, date_func = datetime.date, n_threads = 10):
    '''
    Generate listings.

    In:
        site: Something like "austin.craigslist.org"
        section: Something like "sub"
    Yields:
        dicts of listing information
    '''
    try:
        results = []
        html = None
        warehouse = Warehouse(cachedir)

        while True:
            # Listings
            urls = (result['href'] for result in results)
            for result, url, html in zip(results, *download.download_many(get, warehouse, urls, date_func, n_threads)):
                # result.update(parse.???(html))
                yield result

            # Search
            url = parse.next_search_url(scheme, site, section, html)
            if url is None:
                break
            response = download.download(get, warehouse, url, date_func())
            html = parse.load_response(response)
            results.extend(parse.search(html))
            if results == []:
                break

    except GeneratorExit:
        pass

def sites(get = requests.get, url = 'https://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar', date_func = datetime.date):
    '''
    Generate craigslist sites.
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
            for netloc in sites(get = requests.get, url = href, cachedir = cachedir, id = 'list', date_func = date_func):
                results.add(netloc)
                yield netloc
        elif p.netloc not in results:
            results.add(p.netloc)
            yield p.netloc
