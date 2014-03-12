import os
import concurrent.futures as f
import datetime
from time import sleep
import requests
try:
    from queue import Queue
except ImportError:
    from Queue import Queue

from pickle_warehouse import Warehouse

from craigsgenerator.download import download
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
                        download, datetime.datetime.today)

    if not superthreaded:
        for site in sites:
            for section in sections:
                for listing in get_listings(site, section):
                    yield listing

    else:
        results = Queue()
        def sink_listings(site,section):
            for listing in get_listings(site,section):
                results.put(listing)
            logger.info('Finished %s/%s' % (site,section))

        with f.ThreadPoolExecutor(threads_per_section) as e:
            futures = {}
            for site in sites:
                for section in sections:
                    futures[(site,section)] = e.submit(sink_listings, site, section)
            while not (all(future.done() for future in futures.values()) and results.empty()):
                yield results.get()
                results.task_done()
