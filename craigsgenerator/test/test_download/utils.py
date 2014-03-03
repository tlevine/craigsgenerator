from collections import namedtuple
import datetime

FakeResponse = namedtuple('Response', ['text'])

def fake_get(url):
    return FakeResponse('lalala')

fake_warehouse = {('http://foo.bar','2014/08'): FakeResponse('baz')}
fake_date = datetime.date(2014,3,1)
