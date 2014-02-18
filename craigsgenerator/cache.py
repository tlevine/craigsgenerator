import os
import datetime
import urllib.parse

import requests

def get(cachedir, url, refresh, *args, **kwargs):
    urldir = _url_to_directory(cachedir, url)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)

    dl = lambda: _download(cachedir, url, today, *args, **kwargs)

    if (not os.path.exists(urldir)) or (os.listdir(urldir) == []):
        _dl()

    mostrecent = sorted(filter(lambda f: os.path.isfile(os.path.join(urldir, f)), os.listdir(urldir)))[-1]
    if refresh and datetime.datetime.strptime(mostrecent, '%Y-%m-%d').date() < yesterday:
        _dl()

    return os.path.join(urldir, mostrecent)

def _download(cachedir, url, date, *args, **kwargs):
    directory = _url_to_directory(cachedir, url)
    filename = os.path.join(directory, date.isoformat())
    if not os.path.exists(directory):
        os.makedirs(directory)

    r = requests.get(url, *args, **kwargs)
    with open(filename, 'x') as f:
        f.write(r.text)

def _url_to_directory(cachedir, url):
    p = urllib.parse.urlparse(url)
    if p.query or p.fragment or p.params:
        raise ValueError('query, fragment and params are not allowed.')
    return os.path.join(*([cachedir, p.netloc] + p.path.strip('/').split('/')))
