from collections import namedtuple
import datetime

FakeResponse = namedtuple('Response', ['url', 'text'])

def fake_get(url):
    return FakeResponse('http://chainsaw.thomaslevine.com', 'lalala')

fake_warehouse = {('http://foo.bar','2014/08'): FakeResponse('http://thomaslevine.com', 'baz')}
fake_date = datetime.date(2014,3,1)
