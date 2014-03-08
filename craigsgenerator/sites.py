import requests
def sites(get = requests.get, url = 'https://sfbay.craigslist.org', cachedir = 'craigslist', id = 'rightbar')):
    '''
    Generate craigslist sites.
    '''
    raise NotImplementedError
    results = set()
    warehouse = Warehouse(cachedir)

    response = parse.download(warehouse, url, get)
    html = parse.load_response(response)

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
