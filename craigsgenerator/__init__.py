from queue import Queue
from craigsgenerator.generators import listings as _listings
from craigsgenerator.generators import sites as _sites

def craigsgenerator(sites = _sites, listings = _listings, sections = ['sub'], threaded = True):
    results = Queue()
    def worker(thesite, thesection):
        for listing in thelistings(thesite, thesection):
            results.put(listing)

    if threaded:
        threads = {}

    for site in sites():
        for section in sections:
            if threaded:
                threads[(site, section)] = Thread(None, worker, args = (site, section))
            else:
                worker(thesite, thesection)

    if threaded:
        for thread in threads.values():
            thread.start()
        for thread in threads.values():
            thread.join()

    while not results.empty():
        yield results.get()
