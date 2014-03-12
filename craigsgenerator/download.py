try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
try:
    from queue import Queue
except ImportError:
    from Queue import Queue

def download_one(warehouse, url, get, date):
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

def download_many(warehouse, urls, get, n_threads):
    '''
    Only works for dateless caches
    '''
    def _download_one(url):
        return download_one(warehouse, url, get, None)

    with ThreadPoolExecutor(n_threads) as e:
        for response in e.map(_download_one, urls):
            yield response

def already_downloaded(warehouse, url):
    'Have I already made a similar enough request?'
    return url in warehouse
