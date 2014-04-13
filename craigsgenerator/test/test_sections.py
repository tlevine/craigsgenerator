import os

from nose.tools import assert_list_equal

from pickle_warehouse import Warehouse
from craigsgenerator.sections import sections

def test_sections():
    w = Warehouse(os.path.join('craigsgenerator','test','fixtures','sections'))
    observed = list(sections(warehouse = w))
    expected = ['ccc', 'act', 'ats', 'kid', 'com', 'grp', 'pet', 'eve', 'laf', 'muc', 'vnn', 'pol', 'rid', 'vol', 'cls', 'hhh', 'apa', 'roo', 'sub', 'hsw', 'swp', 'vac', 'prk', 'off', 'rea', 'sss', 'ata', 'baa', 'bar', 'bia', 'boo', 'bka', 'bfa', 'sya', 'zip', 'fua', 'foa', 'hsa', 'jwa', 'maa', 'rva', 'sga', 'tia', 'tla', 'waa', 'ppa', 'ara', 'sna', 'pta', 'haa', 'ema', 'moa', 'cla', 'cba', 'ela', 'gra', 'hva', 'msa', 'pha', 'taa', 'vga', 'bbb', 'bts', 'crs', 'cps', 'cys', 'evs', 'fns', 'lgs', 'lss', 'mas', 'pas', 'aos', 'fgs', 'hss', 'lbs', 'sks', 'rts', 'biz', 'thp', 'trv', 'wet', 'jjj', 'acc', 'ofc', 'egr', 'med', 'sci', 'bus', 'csr', 'edu', 'fbh', 'lab', 'gov', 'hum', 'eng', 'lgl', 'mnu', 'mar', 'hea', 'npo', 'rej', 'ret', 'sls', 'spa', 'sec', 'trd', 'sof', 'sad', 'tch', 'trp', 'tfr', 'web', 'wri', 'etc', 'ggg', 'cwg', 'evg', 'lbg', 'tlg', 'cpg', 'crg', 'dmg', 'wrg', 'res']
    assert_list_equal(observed, expected)
