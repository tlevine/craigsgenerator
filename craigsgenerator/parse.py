SEARCH_ROW_ATTRS = [
    ('href','a/@href', str),
    ('latitude', '@data-latitude', float),
    ('longitude', '@data-longitude', float),
    ('date','span[@class="pl"]/span[@class="date"]/text()', str),
    ('title','span[@class="pl"]/a/text()', str),
    ('price','span[@class="l2"]/span[@class="price"]/text()', lambda x: int(x.strip('$',))),
]

def search_row(p):
    'Parse a <p class="row"></p>.'
    row = {}
    for key, attr, func in SEARCH_ROW_ATTRS:
        results = p.xpath(attr)
        if len(results) == 1:
            row[key] = func(results[0])

    ('href','a/@href'),
    ('latitude', '@data-latitude'),
    ('longitude', '@data-longitude'),
    ('date','span[@class="pl"]/span[@class="date"]/text()'),
    ('title','span[@class="pl"]/a/text()'),
    ('price','span[@class="l2"]/span[@class="price"]/text()'),

    return row

def next_search_url(scheme, subdomain, section, html):
    'Determine the url of the next search page.'
    if html is None:
        return '%s://%s.craigslist.org/%s/index000.html' % (scheme, subdomain, section)

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
