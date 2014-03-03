import requests
from queue import Queue
from craigsgenerator.generators import listings as _listings
from craigsgenerator.generators import sites as _sites

def craigsgenerator(cachedir = 'craigslist', scheme = 'https', get = requests.get,
                    date_func = datetime.date, threads_per_section = 10, superthreaded = True,
                    sites = _sites, listings = _listings, sections = lambda: ['sub']):
    '''
    '''

    results = Queue()
    def worker(thesite, thesection):
        for listing in thelistings(thesite, thesection):
            results.put(listing)

    if superthreaded:
        threads = {}

    for site in sites():
        for section in sections:
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
