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

def listings(scheme, get, n_threads, warehouse, site, section):
    '''
    Generate listings.

    In:
        site: Something like "austin.craigslist.org"
        section: Something like "sub"
    Yields:
        dicts of listing information
    '''
    try:
        html = None
        while True:
            # Listings
            urls = {result['href']:result for result in results}
            for response in download.download_many(get, warehouse, urls, date_func, n_threads):
                result = urls[response.url]
                result.update(parse.listing(response))

                result['html'] = response.text
                result['downloaded'] = datetime_func()
                result['url'] = result['href']
                result['site'] = site
                result['section'] = section

                del(result['href'])
                del(result['date'])
                yield result
            results = []

            # Search
            url = parse.next_search_url(scheme, site, section, html)
            if url == None:
                break
            response = download.download(get, warehouse, url, date_func())
            results = parse.search(response)
            html = lxml.html.fromstring(response.text)
            html.make_links_absolute(url)
            if results == []:
                break

    except GeneratorExit:
        pass
