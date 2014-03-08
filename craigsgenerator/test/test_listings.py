import datetime

import nose.tools as n

import craigsgenerator.test.util as util
from craigsgenerator.listings import listings, _join

fake_response = lambda url: util.FakeResponse(url = url, text = '<a href="%s">Look!</a>' % url)
fake_datetime = datetime.datetime(2014,1,1)

def fake_result(url):
    return {
        'html': fake_response(url).text,
        'downloaded': fake_datetime,
        'url': url,
        'site': 'chicago.craigslist.org',
        'section': 'sub',
    }

def fake_download_many(_, urls, __, ___, ____):
    return (fake_response(url) for url in urls)

def test_listings():
    scheme = 'https'
    gotten = set()
    def get(url):
        gotten.add(url)
        return fake_response(url)
    n_threads = 4
    warehouse = {}
    site = 'chicago.craigslist.org'
    section = 'sub'

    parse_listing = lambda _: {}
    parse_search = lambda _: [{'href':None,'date' :None}]

    searched = set()
    def parse_next_search_url(scheme, site, section, html):
        if html == None:
            searched.clear()
        url = '%s://%s/%s/index%d00.html' % (scheme, site, section, len(searched))
        searched.add(url)
        return url

    l = listings(scheme, get, n_threads, warehouse, site, section,
                 parse_listing, parse_search, parse_next_search_url,
                 fake_download_many, None, lambda: fake_datetime)
    n.assert_set_equal(gotten, set())

    result = next(l)
#   n.assert_equal(result, fake_result('https://chicago.craigslist.org/sub/index000.html'))
    n.assert_set_equal(gotten, {'https://chicago.craigslist.org/sub/index000.html'})

    response = next(l)
#   n.assert_equal(response, fake_result('https://chicago.craigslist.org/sub/index100.html'))
    n.assert_set_equal(gotten, {
        'https://chicago.craigslist.org/sub/index000.html',
        'https://chicago.craigslist.org/sub/index100.html'})

def test_join():
    url = 'http://example.com'
    search_row = {'href': url, 'date': '3 months ago'}
    listing = {'html':'<html></html>'}
    site = 'chicago.craigslist.org'
    section = 'sub'
    datetime_func = lambda: fake_datetime

    observed = _join(search_row, listing, datetime_func, site, section)
    expected = { 'url': url, 'site': site, 'section': section,
        'html': '<html></html>', 'downloaded': datetime_func()}
    n.assert_dict_equal(search_row, {'href': url, 'date': '3 months ago'}) # should not mutate
    n.assert_dict_equal(observed, expected)
