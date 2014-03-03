from string import capwords
import dateutil.parser, datetime

import lxml.html

SEARCH_ROW_ATTRS = [
    ('href','a/@href', str),
    ('latitude', '@data-latitude', float),
    ('longitude', '@data-longitude', float),
    ('date','span[@class="pl"]/span[@class="date"]/text()', str),
    ('title','span[@class="pl"]/a/text()', str),
    ('price','span[@class="l2"]/span[@class="price"]/text()', lambda x: int(x.strip('$',))),
]

def search(response):
    '''
    response ->  [HTML element]
    '''
    html = load_response(response)
    return list(map(search_row,html.xpath('//p[@class="row"]')))

def listing(response):
    '''
    response ->  [HTML element]
    '''
    html = load_response(response)

    def humandate(text):
        ds = html.xpath('//p[contains(text(),"%s") or contains(text(),"%s")]/time/@datetime' % (capwords(text), text.lower()))
        if ds != []:
            e = dateutil.parser.parse(ds[0])
            return datetime.datetime.fromtimestamp((datetime.datetime.astimezone(e).timestamp()))

    return {k:humandate(k) for k in ['posted','updated']}


def search_row(p):
    'Parse a <p class="row"></p>.'
    row = {}
    for key, attr, func in SEARCH_ROW_ATTRS:
        results = p.xpath(attr)
        if len(results) == 1:
            row[key] = func(results[0])

    return row

def next_search_url(scheme, root, section, html):
    '''
    Determine the url of the next search page.
    In:
        scheme: "http" or "https"
        root: something like "boston.craigslist.org"
        section: a section in craigslist ("sub", "jsy/sub", &c.)
        html: lxml HTML element for the current page
    Out:
        A url
    '''
    if html is None:
        return '%s://%s/%s/index000.html' % (scheme, root, section)

    nexts = set(html.xpath('//a[contains(text(),"next >")]/@href'))
    if len(nexts) == 0:
        return None
    elif len(nexts) == 1:
        return str(list(nexts)[0])
    else:
        raise ValueError('Unexpected number of next links (%d)' % (len(nexts)))

def load_response(response):
    '''
    In:  python-requests Response
    Out: lxml HTML tree
    '''
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    return html
