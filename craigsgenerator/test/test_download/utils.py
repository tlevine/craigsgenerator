from collections import namedtuple
import datetime

FakeResponse = namedtuple('Response', ['url', 'text'])

def fake_get(url):
    return FakeResponse('http://chainsaw.thomaslevine.com', 'lalala')

def fake_get_should_not_run(_):
    raise AssertionError('This should not run.')

fake_warehouse = {'http://foo.bar': FakeResponse('http://thomaslevine.com', 'baz')}

def fake_date_func():
    return fake_date
