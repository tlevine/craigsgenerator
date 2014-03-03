from urllib.parse import urlsplit
from itertools import repeat
from threading import Thread
from queue import Queue

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

    key = (url, d.strftime('%Y/%W'))
    if key in warehouse:
        r = warehouse[key]
    else:
        r = get(url)
        warehouse[key] = r
    return r

def already_downloaded(warehouse, url, date):
    'Have I already made a similar enough request?'
    key = (url, d.strftime('%Y/%W'))
    return key in warehouse

def download_many(get, warehouse, urls, date_func, n_threads):
    threads = {}
    results = Queue()

    for url in urls:
        kwargs = {
            'target': threaded_download_worker,
            'name': url,
            'args': (get, warehouse, url, date_func),
        }
        threads['url'] = Thread(None, **kwargs)

    for thread in threads.values():
        thread.start()

    for thread in threads.values():
        thread.join()

    while not queue.empty():
        yield queue.get()

def threaded_download_worker(get, warehouse, url, date_func, target):
    '''
    Send HTML elements to the target queue.
    '''
    response = download.download(get, warehouse, url, date_func())
    html = parse.load_response(response)
    target.put(html)
