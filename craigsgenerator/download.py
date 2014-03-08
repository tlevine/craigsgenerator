try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
from itertools import repeat
from threading import Thread
try:
    from queue import Queue
except ImportError:
    from Queue import Queue

def download(warehouse, url, get, date):
    '''
    In:
        get: function that takes a url and returns a python-requests Response
        warehouse: a pickle_warehouse.Warehouse
        url: a url str
        date: a date string or None, to be added to the key for caching
    Out:
        A python-requests Response
    '''
    if urlsplit(url).scheme not in {'http','https'}:
        raise ValueError('Scheme must be one of "http" or "https".')

    key = url if date == None else (url, date)
    if key in warehouse:
        r = warehouse[key]
    else:
        r = get(url)
        warehouse[key] = r
    return r

def already_downloaded(warehouse, url):
    'Have I already made a similar enough request?'
    return url in warehouse

def threaded_download_worker(warehouse, url, get, target):
    '''
    Send HTML elements to the target queue.
    '''
    response = download(warehouse, url, get, None)
    target.put(response)

def download_many(warehouse, urls, get, n_threads, worker):
    '''
    Only works for dateless caches
    '''
    threads = {}
    results = Queue()

    for url in urls:
        kwargs = {
            'target': worker,
            'name': url,
            'args': (warehouse, url, get, results),
        }
        threads[url] = Thread(None, **kwargs)

    for thread in threads.values():
        thread.start()

    for thread in threads.values():
        thread.join()

    while not results.empty():
        yield results.get()
