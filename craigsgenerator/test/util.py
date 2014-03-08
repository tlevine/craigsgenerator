import os
from collections import namedtuple

FakeResponse = namedtuple('Response', ['url', 'text'])

def read(fn):
    with open(os.path.join('craigsgenerator','test','fixtures',fn)) as fp:
        r = FakeResponse('https://foo.bar/baz', fp.read())
    return r

