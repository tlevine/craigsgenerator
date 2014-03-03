import requests
from queue import Queue
from craigsgenerator.generators import sites, sections, listings

def craigsgenerator(cachedir = 'craigslist', scheme = 'https', get = requests.get,
        date_func = datetime.date, threads_per_section = 10, superthreaded = True):
    '''
    In:
        cachedir: Where should downloads (pickled Response objects) be stored?
        scheme: "https" or "http"
        get: a function that takes a url and returns a Response object
        date_func: a function that returns a datetime.date
        threads_per_section: How many threads to run within each particular craigslist section, by site
        superthreaded: Whether to run each craigslist site in a different thread
    Out:
        A generator of dictionaries
    '''
    kwargs = {
        'cachedir': cachedir, 'scheme': scheme,
        'get': get, 'date_func': date_func,
    }

    results = Queue()
    def worker(thesite, thesection):
        for listing in thelistings(thesite, thesection, n_threads = threads_per_section, **kwargs):
            results.put(listing)

    if superthreaded:
        threads = {}

    for site in sites(**kwargs):
        for section in sections(**kwargs):
            if superthreaded:
                threads[(site, section)] = Thread(None, worker, args = (site, section))
            else:
                worker(thesite, thesection)

    if superthreaded:
        for thread in threads.values():
            thread.start()
        for thread in threads.values():
            thread.join()

    while not results.empty():
        yield results.get()
