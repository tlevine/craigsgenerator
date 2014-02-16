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

def listing(html):
    postingbody = html.get_element_by_id('postingbody')
    return postingbody.text_content()
