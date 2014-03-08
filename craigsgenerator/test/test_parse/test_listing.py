import datetime

import nose.tools as n

import craigsgenerator.parse as parse
import craigsgenerator.test.util as util

def check_listing(fn, expected):
    r = util.read(fn)
    observed = parse.listing(r)
    n.assert_dict_equal(observed, expected)

listing_testcases = [
    ('4212230639.html', {
        'html': util.read('4212230639.html').text,
        'posted':  datetime.datetime(2013, 11, 25,  0, 52, 38) + datetime.timedelta(hours = 5),
        'updated': datetime.datetime(2013, 12,  1, 21, 47, 39) + datetime.timedelta(hours = 5)
    }),
    ('4223403463.html', {
        'html': util.read('4223403463.html').text,
        'posted': datetime.datetime(2013, 12, 1, 18, 16, 46) + datetime.timedelta(hours = 5),
        'updated': None
    }),
]

def test_listing():
    'The listing parser should return a dict  with posted and updated datetimes, in UTC.'
    for fn, expected in listing_testcases:
        yield check_listing, fn, expected
