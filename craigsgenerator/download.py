try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
try:
    basestring
except NameError:
    basestring = str
from functools import partial
from concurrent.futures import ThreadPoolExecutor

def download(get, warehouse, urls, date, n_threads = 10):
    '''
    In:
        get: function that takes a url and returns a python-requests Response
        warehouse: a pickle_warehouse.Warehouse
        url: a url str or an iterable of urls
        date: a date string or None, to be added to the key for caching
    Out:
        A python-requests Response
    '''
    one_url = isinstance(urls,basestring)
    if one_url:
        urls = [urls]

    func = partial(parallel, n_threads) if n_threads > 1 else serial
    generator = func(get, warehouse, urls, date)

    if one_url:
        return next(generator)
    else:
        return generator

def serial(get, warehouse, urls, date):
    for url in urls:
        if urlsplit(url).scheme not in {'http','https'}:
            raise ValueError('Scheme must be one of "http" or "https".')

        key = url if date == None else (url, date)
        if key in warehouse:
            r = warehouse[key]
        else:
            r = get(url)
            warehouse[key] = r
        yield r

def parallel(n_threads, get, warehouse, urls, date):
    def _download_one(url):
        return next(serial(get, warehouse, [url], date))

    with ThreadPoolExecutor(n_threads) as e:
        for response in e.map(_download_one, urls):
            yield response

def already_downloaded(warehouse, url):
    'Have I already made a similar enough request?'
    return url in warehouse
