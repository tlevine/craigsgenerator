import os
from threading import Thread
import datetime
from time import sleep
import requests
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

from pickle_warehouse import Warehouse

import craigsgenerator.download as download
import craigsgenerator.parse as parse
from craigsgenerator.listings import listings as _listings
from craigsgenerator.sites import sites as _sites
from craigsgenerator.sections import sections as _sections

def craigsgenerator(sites = None, sections = None, listings = _listings,
                    cachedir = 'craigslist', scheme = 'https',
                    get = requests.get,
                    threads_per_section = 10, superthreaded = True):
    '''
    These parameters limit what pages will be downloaded; if you use the defaults, all pages will be downloaded.
        sites: An iterable of Craigslist sites to download (like "boston.craigslist.org")
        sections: An iterable of Craigslist sites to download (like "roo" or "sub")

    The rest of the paramaters relate to the manner of download.
        cachedir (str): Where should downloads (pickled Response objects) be stored?
        scheme (str): "https" or "http"
        get: a function that takes a url and returns a Response object
        threads_per_section (int): How many threads to run within each particular craigslist section, by site
        superthreaded (bool): Whether to run each craigslist site in a different thread

    Output:
        A generator of dictionaries
    '''
    sleep_interval = 1
    kwargs = {
        'cachedir': cachedir, 'scheme': scheme,
        'get': get,
    }

    if sites == None:
        kwargs_sites = dict(kwargs)
        del(kwargs_sites['scheme'])
        sites = _sites(**kwargs)
    if sections == None:
        sections = _sections(**kwargs)

    warehouse = Warehouse(os.path.join(cachedir, 'listings'))
    def get_listings(site, section):
        return listings(scheme, get, threads_per_section, warehouse, site, section,
                        parse.listing, parse.search, parse.next_search_url,
                        download.download_many, download.threaded_download_worker, datetime.datetime.today)

    if not superthreaded:
        for site in sites:
            for section in sections:
                for listing in get_listings(site, section):
                    yield listing

    else:
        threads = {}
        results = Queue()
        def worker(thesite, thesection):
            for listing in get_listings(thesite, thesection):
                results.put(listing)

        for site in sites:
            for section in sections:
                threads[(site, section)] = Thread(None, worker, args = (site, section))
        for thread in threads.values():
            thread.start()

        while True:
            try:
                yield results.get_nowait()
            except Empty:
                if set(thread.is_alive() for thread in threads.values()) == {False}:
                    break
                else:
                    sleep(sleep_interval)
            else:
                results.task_done()
