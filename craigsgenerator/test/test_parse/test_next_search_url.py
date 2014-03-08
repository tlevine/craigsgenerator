import os

import nose.tools as n
import lxml.html

import craigsgenerator.parse as parse

def check_next_search_url(fn, domain, url):
    with open(os.path.join('craigsgenerator','test','fixtures',fn)) as fp:
        html = lxml.html.fromstring(fp.read())
    html.make_links_absolute(url)
    observed = parse.next_search_url('https', domain, 'sub', html)
    n.assert_equal(observed, url)

def test_next_search_url():
    testcases = [
        ('austin-sub.html', 'austin.craigslist.org', 'https://austin.craigslist.org/sub/index100.html'),
        ('chicago-sub.html', 'chicago.craigslist.org', 'https://chicago.craigslist.org/sub/index100.html'),
    ]
    for fn, domain, url in testcases:
        yield check_next_search_url, fn, domain, url
