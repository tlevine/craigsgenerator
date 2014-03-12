import re
import os
try:
    from urllib.parse import urlparse
except ImportError:
    from urllib2 import urlparse
import datetime

import lxml.html
import requests
from pickle_warehouse import Warehouse

import craigsgenerator.download as download
import craigsgenerator.parse as parse

def listings(scheme, get, n_threads, warehouse, site, section,
             parse_listing, parse_search, parse_next_search_url,
             download, datetime_func):
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
        while True:
            # Listings
            urls = [result['href'] for result in results]
            for response in download(get, warehouse, urls, None, n_threads = n_threads):
                yield _join(response, parse_listing(response), datetime_func, site, section)
            results = []

            # Search
            url = parse_next_search_url(scheme, site, section, html)
            if url == None:
                break

            # use a day-old cache
            print(url)
            response = download(get, warehouse, url, datetime_func().date().isoformat())

            results = parse_search(response)
            html = lxml.html.fromstring(response.text)
            html.make_links_absolute(url)
            if results == []:
                break

    except GeneratorExit:
        pass

def _one_listing():
    pass

def _join(search_dict, listing_dict, datetime_func, site, section):
    r = dict(search_dict)
    r.update(listing_dict)

    r['downloaded'] = datetime_func()
    r['url'] = r['href']
    r['site'] = site
    r['section'] = section

    del(r['href'])
    del(r['date'])
    return r
