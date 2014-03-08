import nose.tools as n

from craigsgenerator.download import download_many
import craigsgenerator.test.test_download.utils as utils

def fake_worker(warehouse, url, get, target):
    target.put(utils.FakeResponse(url, 'blah'))

def test_download_many():
    warehouse = {}
    urls = ['http://foo', 'https://bar', 'http://example.com']
    observed = set(download_many(warehouse, urls, utils.fake_get_should_not_run, urls, fake_worker))
    expected = set(utils.FakeResponse(url, 'blah') for url in urls)
    n.assert_set_equal(observed, expected)
