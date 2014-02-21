import re
import os
import urllib.parse
#from logging import Logger
import datetime

import lxml.html

from craigsgenerator.cache import get
from craigsgenerator.parse import search_row

#logger = Logger('craigsgenerator')

class Section:
    def __init__(self, subdomain, section, *args, cachedir = 'craigslist', scheme = 'https', **kwargs):
        if scheme not in {'http','https'}:
            raise ValueError('Scheme must be one of "http" or "https".')

        self.subdomain = subdomain
        self.section = section
        self.cachedir = cachedir
        self.args = args
        self.kwargs = kwargs
        self.scheme = scheme

    def __iter__(self):
        self.buffer = []
        self.html = None
        self.present_search_url = None
        return self

    def __next__(self):
        if self.buffer == []:
            if self.next_search_url() is None:
            #   logger.debug('Stopped at %s' % self.present_search_url)
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

    def bump_url(self):
        url = self.next_search_url()
        if url is None:
            raise ValueError('No next page for %s' % self.present_search_url)
        self.present_search_url = url

    def download(self):
        with open(get(self.cachedir, self.present_search_url, True, *self.args, **self.kwargs)) as fp:
            html = lxml.html.fromstring(fp.read())
        html.make_links_absolute(self.present_search_url)
        self.html = html

    def skip_downloaded(self):
        'Skip the things that have been downloaded; start iterating at things that have not been downloaded.'
        today = datetime.date.today()
        yesterday = datetime.date.today()

        sectiondir = os.path.join(self.cachedir, self.subdomain + '.craigslist.org', self.section)
        for index in sorted(filter(lambda x: x.startswith('index'), filter(os.path.isdir, os.listdir(sectiondir)))):
            url = os.path.join(sectiondir, index)
            if os.path.exists(os.path.join(url, today)) or os.path.exists(os.path.join(url, yesterday)):
                self.present_search_url = '%s://%s.craigslist.org/%s/%s' % (self.scheme, self.subdomain, self.section, index)
            else:
                break
        if self.present_search_url is not None:
            self.download()

    def next_search_url(self):
        'Determine the url of the next search page.'
        if self.html is None:
            return '%s://%s.craigslist.org/%s/index000.html' % (self.scheme, self.subdomain, self.section)

        nexts = set(self.html.xpath('//a[contains(text(),"next >")]/@href'))
        if len(nexts) == 0:
            return None
        elif len(nexts) == 1:
            return str(list(nexts)[0])
        else:
            raise ValueError('Unexpected number of next links (%d) at %s' % (len(nexts), self.present_search_url))

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

def tohtml(row):
    'Given a row from the Section generator, produce the full text of the listing.'
    with open(row['listing']) as fp:
        html = lxml.html.fromstring(fp.read())
    return html
