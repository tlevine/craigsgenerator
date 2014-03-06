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

def download(get, warehouse, url, date):
    '''
    In:
        get: function that takes a url and returns a python-requests Response
        warehouse: a pickle_warehouse.Warehouse
        url: a url str
        date: a datetime.date
    Out:
        A python-requests Response
    '''
    if urlsplit(url).scheme not in {'http','https'}:
        raise ValueError('Scheme must be one of "http" or "https".')

    key = (url, date.strftime('%Y/%W'))
    if key in warehouse:
        r = warehouse[key]
    else:
        r = get(url)
        warehouse[key] = r
    return r

def already_downloaded(warehouse, url, date):
    'Have I already made a similar enough request?'
    key = (url, date.strftime('%Y/%W'))
    return key in warehouse

def threaded_download_worker(get, warehouse, url, date_func, target):
    '''
    Send HTML elements to the target queue.
    '''
    response = download(get, warehouse, url, date_func())
    target.put(response)

def download_many(get, warehouse, urls, date_func, n_threads, worker = threaded_download_worker):
    '''
    '''
    threads = {}
    results = Queue()

    for url in urls:
        kwargs = {
            'target': worker,
            'name': url,
            'args': (get, warehouse, url, date_func, results),
        }
        threads[url] = Thread(None, **kwargs)

    for thread in threads.values():
        thread.start()

    for thread in threads.values():
        thread.join()

    while not results.empty():
        yield results.get()
