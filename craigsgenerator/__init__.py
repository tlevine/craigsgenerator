import re

import lxml.html

from craigsgenerator.cache import get
from craigsgenerator.parse import search_row

class Section:
    def __init__(self, subdomain, section, *args, cachedir = 'craigslist', **kwargs):
        self.subdomain = subdomain
        self.section = section
        self.cachedir = cachedir
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        self.buffer = []
        self.html = None
        self.present_search_url = None
        return self

    def __next__(self):
        if self.buffer == []:
            self.download()
            self.buffer.extend(map(search_row,self.html.xpath('//p[@class="row"]')))

        if self.html.xpath('count(//p[@class="row"])') == 0:
            logger.debug('Stopped at %s' % self.present_search_url)
            raise StopIteration
        else:
            row = self.buffer.pop(0)
            row['listing'] = get(self.cachedir, row['href'],
                                 False, *self.args, **self.kwargs)
            return row

    def download(self):
        self.present_search_url = self.next_search_url()
        fp = get(self.cachedir, self.present_search_url, True, *self.args, **self.kwargs)

        html = lxml.html.fromstring(fp.read())
        html.make_links_absolute(self.present_search_url)
        self.html = html

    def next_search_url(self):
        'Determine the url of the next search page.'
        if not self.html:
            return 'https://%s.craigslist.org/%s/index000.html' % (self.subdomain, self.section)

        nexts = set(self.html.xpath('//a[contains(text(),"next >")]/@href'))
        if len(nexts) != 1:
            raise ValueError('No next page for %s' % self.search_url)
        return str(list(nexts)[0])
