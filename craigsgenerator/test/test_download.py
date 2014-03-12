import nose.tools as n
from collections import namedtuple
import datetime

from craigsgenerator.download import download_one, download_many

FakeResponse = namedtuple('Response', ['url', 'text'])

def fake_get(url):
    return FakeResponse('http://chainsaw.thomaslevine.com', 'lalala')

def fake_get_should_not_run(_):
    raise AssertionError('This should not run.')

fake_warehouse = {'http://foo.bar': FakeResponse('http://thomaslevine.com', 'baz')}

fake_warehouse_with_date = {('http://foo.bar','2014-03-01'): FakeResponse('http://thomaslevine.com', 'baz')}

def fake_date_func():
    return fake_date

def check_bad_scheme(download):
    with n.assert_raises(ValueError):
        r = download(fake_warehouse, 'ftp://example.com', fake_get, None)

def check_cached(download):
    r = download(fake_warehouse, 'http://foo.bar', fake_get, None)
    n.assert_equal(r.text, 'baz')

def test_cached_with_date():
    r = download_one(fake_warehouse_with_date, 'http://foo.bar', fake_get_should_not_run, '2014-03-01')
    n.assert_equal(r.text, 'baz')
    r = download_one(fake_warehouse_with_date, 'http://foo.bar', fake_get, '2014-03-02')
    n.assert_equal(r.text, 'lalala')

def check_not_cached(download):
    d = {}
    r = download(d, 'http://foo.bar', fake_get, None)
    n.assert_equal(r.text, 'lalala')
    n.assert_dict_equal(d, {'http://foo.bar': fake_get(None)})

_download_many = lambda warehouse, url, get, date: download_many(warehouse, [url], get, 2)

def test_bad_scheme():
    for download in download_one, _download_many:
        yield check_bad_scheme, download
def test_cached():
    for download in download_one, _download_many:
        yield check_cached, download
def test_not_cached():
    for download in download_one, _download_many:
        yield check_not_cached, download
