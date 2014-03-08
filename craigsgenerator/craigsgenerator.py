import datetime
from time import sleep
import requests
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

import craigsgenerator.generators as g

def craigsgenerator(sites = None, sections = None,
                    cachedir = 'craigslist', scheme = 'https', get = requests.get,
                    date_func = datetime.date.today, threads_per_section = 10,
                    superthreaded = True, sleep_interval = 1):
    '''
    These parameters limit what pages will be downloaded; if you use the defaults, all pages will be downloaded.
        sites: An iterable of Craigslist sites to download (like "boston.craigslist.org")
        sections: An iterable of Craigslist sites to download (like "roo" or "sub")

    The rest of the paramaters relate to the manner of download.
        cachedir (str): Where should downloads (pickled Response objects) be stored?
        scheme (str): "https" or "http"
        get: a function that takes a url and returns a Response object
        date_func: a function that returns a datetime.date
        threads_per_section (int): How many threads to run within each particular craigslist section, by site
        superthreaded (bool): Whether to run each craigslist site in a different thread
        sleep_interval (int): How long to sleep when waiting for results

    Output:
        A generator of dictionaries
    '''
    try:
        kwargs = {
            'cachedir': cachedir, 'scheme': scheme,
            'get': get, 'date_func': date_func,
        }

        if sites == None:
            kwargs_sites = dict(kwargs)
            del(kwargs_sites['scheme'])
            sites = g.sites(**kwargs)
        if sections == None:
            sections = g.sections(**kwargs)

        if not superthreaded:
            for site in sites:
                for section in sections:
                    for listing in g.listings(site, section, n_threads = threads_per_section, **kwargs):
                        yield listing

        else:
            results = Queue()
            def worker(thesite, thesection):
                for listing in g.listings(thesite, thesection, n_threads = threads_per_section, **kwargs):
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

    except GeneratorExit:
        pass
