import datetime

import nose.tools as n

import craigsgenerator.test.util as util
from craigsgenerator.listings import listings

fake_response = lambda url: util.FakeResponse(url = url, text = '<a href="%s">Look!</a>' % url)
fake_datetime = datetime.datetime(2014,1,1)

def fake_download_many(_, urls, __, ___, ____):
    return (fake_response(url) for url in urls)

def test_listings():
    scheme = 'https'
    gotten = []
    def get(url):
        gotten.append(url)
        return fake_response(url)
    n_threads = 4
    warehouse = {}
    site = 'chicago.craigslist.org'
    section = 'sub'

    parse_listing = lambda _: {}
    parse_search = lambda _: [{'href':None,'date' :None}]

    def parse_next_search_url(scheme, site, section, html, searched_urls = 0):
        if html == None:
            searched_urls *= 0
        url = '%s://%s/%s/index%03d.html' % (scheme, site, section, searched_urls)
        searched_urls += 1
        return url

    l = listings(scheme, get, n_threads, warehouse, site, section,
                 parse_listing, parse_search, parse_next_search_url,
                 fake_download_many, None, lambda: fake_datetime)
    n.assert_list_equal(gotten, [])

    response = next(l)
    n.assert_equal(response, fake_response('https://chicago.craigslist.org/sub/index000.html'))
    n.assert_list_equal(gotten, ['https://chicago.craigslist.org/sub/index000.html'])

    response = next(l)
    n.assert_equal(response, fake_response('https://chicago.craigslist.org/sub/index100.html'))
    n.assert_list_equal(gotten, [
        'https://chicago.craigslist.org/sub/index000.html',
        'https://chicago.craigslist.org/sub/index100.html'])
