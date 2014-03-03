from collections import namedtuple
import datetime

FakeResponse = namedtuple('Response', ['url', 'text'])

def fake_get(url):
    return FakeResponse('http://chainsaw.thomaslevine.com', 'lalala')

def fake_get_should_not_run(_):
    raise AssertionError('This should not run.')

fake_datestring = '2014/08'
fake_date = datetime.date(2014,3,1)
fake_warehouse = {('http://foo.bar',fake_datestring): FakeResponse('http://thomaslevine.com', 'baz')}

def fake_date_func():
    return fake_date
