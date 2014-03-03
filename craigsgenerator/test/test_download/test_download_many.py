import nose.tools as n

from craigsgenerator.download import download_many
import craigsgenerator.test.test_download.utils as utils

def fake_worker(get, warehouse, url, date_func, target):
    target.put(utils.FakeResponse(url, 'blah'))

def test_download_many():
    warehouse = {}
    urls = ['http://foo', 'https://bar', 'http://example.com']
    observed = set(download_many(utils.fake_get_should_not_run, warehouse,
                   urls, lambda: utils.fake_date, 4, worker = fake_worker))
    expected = set(utils.FakeResponse(url, 'blah') for url in urls)
    n.assert_set_equal(observed, expected)
