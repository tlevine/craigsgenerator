import os
import datetime
import urllib.parse

import requests

def get(url, refresh = False):
    urldir = _url_to_directory(url)
    if (not os.path.exists(urldir)) or os.listdir(urldir) == []:
        _download(url)

    mostrecent = sorted(os.listdir(urldir))[-1]
    if refresh and datetime.datetime.strptime(mostrecent, '%Y-%m-%d').date() < datetime.datetime.today():
        _download(url)

    return open(os.path.join(urldir, mostrecent), 'r')

def _download(url, date = datetime.date.today()):
    directory = _url_to_directory(url)
    filename = os.path.join(directory, date.isoformat())
    if not os.path.exists(directory):
        os.makedirs(directory)

    r = requests.get(url, headers = HEADERS)
    with open(filename, 'x') as f:
        f.write(r.text)

def _url_to_directory(url):
    p = urllib.parse.urlparse(url)
    if p.query or p.fragment or p.params:
        raise ValueError('query, fragment and params are not allowed.')
    return os.path.join(*(['cache', p.netloc] + p.path.strip('/').split('/')))
