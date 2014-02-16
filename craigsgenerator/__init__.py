import re

import lxml.html

from craigsgenerator.cache import get

class Section:
    def __init__(self, subdomain):
        self.subdomain = subdomain

    def __iter__(self):
        self.buffer = []
        self.html = None
        self.present_search_url = None
        return self

    def __next__(self):
        if self.buffer == []:
            self.download()
            self.buffer.extend(map(str,self.html.xpath('//p[@class="row"]/a/@href')))

        if self.html.xpath('count(//p[@class="row"])') == 0:
            logger.debug('Stopped at %s' % self.present_search_url)
            raise StopIteration
        else:
            return self.buffer.pop(0)

    def download(self):
        self.present_search_url = self.next_search_url()
        fp = get(self.present_search_url)

        html = lxml.html.fromstring(fp.read())
        html.make_links_absolute(self.present_search_url)
        self.html = html

    def next_search_url(self):
        'Determine the url of the next search page.'
        if not self.html:
            return 'https://%s.craigslist.org/sub/index000.html' % self.subdomain

        nexts = set(self.html.xpath('//a[contains(text(),"next >")]/@href'))
        if len(nexts) != 1:
            raise ValueError('No next page for %s' % self.search_url)
        return str(list(nexts)[0])
