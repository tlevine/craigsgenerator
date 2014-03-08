import nose.tools as n

from craigsgenerator.download import download
import craigsgenerator.test.test_download.utils as utils

def test_bad_scheme():
    with n.assert_raises(ValueError):
        r = download(utils.fake_warehouse, 'ftp://example.com', utils.fake_get)

def test_cached():
    r = download(utils.fake_warehouse, 'http://foo.bar', utils.fake_get)
    n.assert_equal(r.text, 'baz')

def test_not_cached():
    d = {}
    r = download(d, 'http://foo.bar', utils.fake_get)
    n.assert_equal(r.text, 'lalala')
    n.assert_dict_equal(d, {'http://foo.bar': utils.fake_get(None)})
