from queue import Queue

import nose.tools as n

from craigsgenerator.download import threaded_download_worker
import craigsgenerator.test.test_download.utils as utils


def test():
    warehouse = {'http://blah': 'zombies'}
    queue = Queue()
    threaded_download_worker(utils.fake_get_should_not_run,
            warehouse, 'http://blah', utils.fake_date_func, queue)
    n.assert_false(queue.empty())
    n.assert_equal(queue.get(), 'zombies')
    n.assert_true(queue.empty())
