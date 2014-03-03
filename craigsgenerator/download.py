from urllib.parse import urlsplit

def _cache(get, warehouse, url, date):
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

def can_i_skip(warehouse, url, date):
    'Can I skip the present request?'
    key = (url, d.strftime('%Y/%W'))
    return key in warehouse
