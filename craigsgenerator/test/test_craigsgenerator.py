import nose.tools as n

from craigsgenerator.craigsgenerator import craigsgenerator

def test_craigsgenerator():
    cg = craigsgenerator(sites = ['foo'], sections = ['bar'], listings = lambda *args, **kwargs: ['baz'])
    n.assert_equal(next(cg), 'baz')
#   with n.assert_raises(StopIteration):
#       next(cg)
