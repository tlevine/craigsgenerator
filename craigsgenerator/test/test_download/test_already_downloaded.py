import datetime

import nose.tools as n

from craigsgenerator.download import already_downloaded

url = 'http://thomaslevine.com/!'
date = datetime.date(2013, 2, 1)
datestring = '2013/04'

def test_yes():
    warehouse = {(url, datestring): 'this string doesn\'t matter.'}
    n.assert_true(already_downloaded(warehouse, url, date))

def test_no():
    warehouse = {}
    n.assert_false(already_downloaded(warehouse, url, date))

