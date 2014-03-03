from collections import namedtuple
import datetime

import nose.tools as n

from craigsgenerator.download import download

FakeResponse = namedtuple('Response', ['text'])

def fake_get(url):
    return FakeResponse('lalala')

fake_warehouse = {'http://foo.bar': 'baz'}
fake_date = datetime.date(2014,3,1)

def test_bad_scheme():
    with n.assert_raises(ValueError):
        r = download(fake_get, fake_warehouse, 'ftp://example.com', fake_date)
