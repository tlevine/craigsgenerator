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


'''
 <p class="row" data-latitude="30.174300" data-longitude="-97.822500" data-pid="4328170456">
    <a href="/sub/4328170456.html" class="i" data-id="0:00V0V_bJm3ol0z8rY" </a>
    <span class="star"></span>
    <span class="pl">
        <span class="date">Feb 15</span>
        <a href="/sub/4328170456.html">**Exceptional LIVING - 2bd/ 2ba LUXURY</a>
    </span>
    <span class="l2">
        <span class="price">&#x0024;1400</span>
        / 2br - 1230ft&sup2; -
        <span class="pnr"> <small> (austin)</small>
            <span class="px">
                <span class="p"> pic&nbsp;
                    <a href="#" class="maptag" data-pid="4328170456">map</a></span></span> </span>  </span> </p>
'''
