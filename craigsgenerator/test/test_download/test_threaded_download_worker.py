import nose.tools as n

from craigsgenerator.download import download
import craigsgenerator.test.test_download.utils as utils


    def threaded_download_worker(utils.fake_get, warehouse, url, date_func, target):
        '''
        Send HTML elements to the target queue.
        '''
        response = download(get, warehouse, url, date_func())
        target.put((url, response))

