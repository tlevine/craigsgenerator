import re
import os
import urllib.parse
import datetime

import lxml.html
from pickle_warehouse import Warehouse

from craigsgenerator.parse import search_row

#logger = Logger('craigsgenerator')

def section(subdomain, section, cachedir = 'craigslist', scheme = 'https', get = requests.get):
    try:
        if scheme not in {'http','https'}:
            raise ValueError('Scheme must be one of "http" or "https".')

        buffer = []
        html = None
        present_search_url = None
        while True:
            if next_search_url(scheme, subdomain, section, html) is None:
                raise StopIteration

            self.bump_url()
            self.download()
            self.buffer.extend(map(search_row,self.html.xpath('//p[@class="row"]')))
            if self.buffer == []:
                raise StopIteration

        row = self.buffer.pop(0)
        row['listing'] = get(self.cachedir, row['href'],
                             False, *self.args, **self.kwargs)
        return row

    except GeneratorExit:
        pass


def subdomains(url = 'https://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar'):
    results = set()
    with open(get(cachedir, url, False)) as fp:
        html = lxml.html.fromstring(fp.read())

    for href in html.xpath('id("%s")/descendant::a/@href' % id):
        p = urllib.parse.urlparse(href.rstrip('/'))
        if p.fragment:
            pass
        elif p.path:
            results.update(subdomains(url = href, cachedir = cachedir, id = 'list'))
        else:
            results.add(p.netloc)
    return results

def bump_url(scheme, subdomain, section, html):
    url = next_search_url(scheme, subdomain, section, html)
    if url is None:
        raise ValueError('No next page')
    return url
