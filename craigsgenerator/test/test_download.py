import nose.tools as n
from collections import namedtuple
import datetime

from craigsgenerator.download import download

FakeResponse = namedtuple('Response', ['url', 'text'])

def fake_get(url):
    return FakeResponse('http://chainsaw.thomaslevine.com', 'lalala')

def fake_get_should_not_run(_):
    raise AssertionError('This should not run.')

fake_warehouse = {'http://foo.bar': FakeResponse('http://thomaslevine.com', 'baz')}

fake_warehouse_with_date = {('http://foo.bar','2014-03-01'): FakeResponse('http://thomaslevine.com', 'baz')}

def fake_date_func():
    return fake_date

def check_bad_scheme(n_threads):
    with n.assert_raises(ValueError):
        next(download(fake_get, fake_warehouse, ['ftp://example.com'], None, n_threads = n_threads))

def check_cached(n_threads):
    r = next(download(fake_get, fake_warehouse, ['http://foo.bar'], None, n_threads = n_threads))
    n.assert_equal(r.text, 'baz')

def check_cached_with_date(n_threads):
    r = next(download(fake_get_should_not_run, fake_warehouse_with_date, ['http://foo.bar'], '2014-03-01', n_threads = n_threads))
    n.assert_equal(r.text, 'baz')
    r = next(download(fake_get, fake_warehouse_with_date, ['http://foo.bar'], '2014-03-02', n_threads = n_threads))
    n.assert_equal(r.text, 'lalala')

def check_not_cached(n_threads):
    d = {}
    r = next(download(fake_get, d, ['http://foo.bar'], None, n_threads = n_threads))
    n.assert_equal(r.text, 'lalala')
    n.assert_dict_equal(d, {'http://foo.bar': fake_get(None)})

def test_bad_scheme():
    yield check_bad_scheme, 5
    yield check_bad_scheme, 1
def test_cached():
    yield check_cached, 5
    yield check_cached, 1
def test_cached_with_date():
    yield check_cached_with_date, 5
    yield check_cached_with_date, 1
def test_not_cached():
    yield check_not_cached, 5
    yield check_not_cached, 1
