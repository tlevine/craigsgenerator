import nose.tools as n

from craigsgenerator.craigsgenerator import craigsgenerator

def test_not_superthreaded():
    cg = craigsgenerator(sites = ['foo'], sections = ['bar'], listings = lambda *args, **kwargs: ['baz'], superthreaded = False)
    n.assert_equal(next(cg), 'baz')
    with n.assert_raises(StopIteration):
        next(cg)

def test_superthreaded():
    cg = craigsgenerator(sites = ['foo'], sections = ['bar'], listings = lambda *args, **kwargs: ['baz'], superthreaded = True)
    n.assert_equal(next(cg), 'baz')
    with n.assert_raises(StopIteration):
        next(cg)
