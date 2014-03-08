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
    warehouse = {url: content}
    queue = Queue()
    threaded_download_worker(warehouse, url, utils.fake_get_should_not_run, queue)
    n.assert_false(queue.empty())
    n.assert_equal(queue.get(), content)
    n.assert_true(queue.empty())
