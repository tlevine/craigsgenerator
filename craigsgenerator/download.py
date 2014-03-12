try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
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
    if isinstance(urls, str):
        one_url = True
        urls = [urls]
    func = partial(parallel, n_threads) if n_threads > 1 else serial
    results = func(get, warehouse, urls, date)
    return results[0] if one_url else results

def serial(warehouse, urls, get, date):
    if urlsplit(url).scheme not in {'http','https'}:
        raise ValueError('Scheme must be one of "http" or "https".')

    key = url if date == None else (url, date)
    if key in warehouse:
        r = warehouse[key]
    else:
        r = get(url)
        warehouse[key] = r
    return r

def parallel(n_threads, get, warehouse, urls, date):
    def _download_one(url):
        return download_one(get, warehouse, url, date)

    with ThreadPoolExecutor(n_threads) as e:
        for response in e.map(_download_one, urls):
            yield response

def already_downloaded(warehouse, url):
    'Have I already made a similar enough request?'
    return url in warehouse
