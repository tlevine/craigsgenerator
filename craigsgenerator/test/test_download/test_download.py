import nose.tools as n

from craigsgenerator.download import download
import craigsgenerator.test.test_download.util as util

def test_bad_scheme():
    with n.assert_raises(ValueError):
        r = download(util.fake_warehouse, 'ftp://example.com', util.fake_get, None)

def test_cached():
    r = download(util.fake_warehouse, 'http://foo.bar', util.fake_get, None)
    n.assert_equal(r.text, 'baz')

def test_cached_with_date():
    r = download(util.fake_warehouse_with_date, 'http://foo.bar', util.fake_get, '2014-03-01')
    n.assert_equal(r.text, 'baz')

def test_not_cached():
    d = {}
    r = download(d, 'http://foo.bar', util.fake_get, None)
    n.assert_equal(r.text, 'lalala')
    n.assert_dict_equal(d, {'http://foo.bar': util.fake_get(None)})
