import requests
import lxml.html

from craigsgenerator.download import download

def sites(get = requests.get, url = 'http://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar'):
    '''
    Generate craigslist sites.
    '''
    raise NotImplementedError
    results = set()
    warehouse = Warehouse(cachedir)

    response = download(get, warehouse, url, None)
    html = lxml.html.fromstring(response.text)

    for href in html.xpath('id("%s")/descendant::a/@href' % id):
        p = urlparse(href.rstrip('/'))
        if p.fragment:
            pass
        elif p.path:
            for netloc in sites(get = requests.get, url = href, cachedir = cachedir, id = 'list'):
                results.add(netloc)
                yield netloc
        elif p.netloc not in results:
            results.add(p.netloc)
            yield p.netloc
