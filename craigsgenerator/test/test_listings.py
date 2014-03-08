import craigsgenerator.test.util as util

fake_response = lambda url: util.FakeResponse(url, '<a href="%s">Look!</a>' % url)

def test_listings():
    scheme = 'https'
    gotten = []
    def get(url):
        gotten.append(url)
        return fake_response
    n_threads = 4
    warehouse = {}
    site = 'chicago.craigslist.org'
    section = 'sub'

    l = listings(scheme, get, n_threads, warehouse, site, section)
    n.assert_list_equal(gotten, [])

    response = next(l)
    n.assert_equal(response, fake_response('https://chicaho.craigslist.org/sub/index000.html'))
    n.assert_list_equal(gotten, ['https://chicaho.craigslist.org/sub/index000.html'])

    response = next(l)
    n.assert_equal(response, fake_response('https://chicaho.craigslist.org/sub/index100.html'))
    n.assert_list_equal(gotten, [
        'https://chicaho.craigslist.org/sub/index000.html',
        'https://chicaho.craigslist.org/sub/index100.html'])
