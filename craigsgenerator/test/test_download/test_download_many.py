import nose.tools as n

from craigsgenerator.download import download_many

def fake_get(url):
    return FakeResponse('lalala')

fake_warehouse = {('http://foo.bar','2014/08'): FakeResponse('baz')}
fake_date = datetime.date(2014,3,1)

def test_cached(get, warehouse, urls, date_func, n_threads):

def test_bad_scheme():
    with n.assert_raises(ValueError):
        r = download(fake_get, fake_warehouse, 'ftp://example.com', fake_date)

def test_cached():
    r = download(fake_get, fake_warehouse, 'http://foo.bar', fake_date)

