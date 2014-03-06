try:
    from queue import Queue
except ImportError:
    from Queue import Queue

import nose.tools as n

from craigsgenerator.download import threaded_download_worker
import craigsgenerator.test.test_download.utils as utils

url = 'http://blah'
content = 'zombies'

def test():
    warehouse = {(url, utils.fake_datestring): content}
    queue = Queue()
    threaded_download_worker(utils.fake_get_should_not_run,
            warehouse, url, utils.fake_date_func, queue)
    n.assert_false(queue.empty())
    n.assert_equal(queue.get(), (url, content))
    n.assert_true(queue.empty())
