import os
import datetime
import urllib.parse

import requests

def get(cachedir, url, refresh, *args, **kwargs):
    urldir = _url_to_directory(cachedir, url)
    if (cachedir == None) or (not os.path.exists(urldir)) or (os.listdir(urldir) == []):
        _download(cachedir, url, *args, **kwargs)

    mostrecent = sorted(os.listdir(urldir))[-1]
    if refresh and datetime.datetime.strptime(mostrecent, '%Y-%m-%d').date() < datetime.date.today():
        _download(cachedir, url, *args, **kwargs)

    return open(os.path.join(urldir, mostrecent), 'r')

def _download(cachedir, url, date = datetime.date.today(), *args, **kwargs):
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
