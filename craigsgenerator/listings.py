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
             download_many, threaded_download_worker,
             datetime_func):
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
            urls = {result['href']:result for result in results}
            responses = download_many(warehouse, urls, get, n_threads, download.threaded_download_worker)
            for response in responses:
                yield _join(urls[response.url], parse_listing(response), datetime_func, site, section)
            results = []

            # Search
            url = parse_next_search_url(scheme, site, section, html)
            if url == None:
                break
            response = download.download(warehouse, url, get)
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
