Craig's Generator
======
Read listings Pythonically.

Examples
---------
Generate listings. ::

    from craigsgenerator import Section
    for listing in Section('oakland','sub'):
        print(listing)

Additional arguments get passed to ``requests.get``. ::

    from craigsgenerator import Section
    proxies = {'https':'example.com'}
    for listing in Section('oakland','sub', proxies = proxies):
        print(listing)

Downloaded files are cached by default and refreshed
if they're older than a day. Change the directory by
specifying the ``cachedir``. ::

    from craigsgenerator import Section
    for listing in Section('oakland','sub', cachedir = 'downloads'):
        print(listing)

Disable caching by setting the ``cachedir`` to ``None``. ::

    from craigsgenerator import Section
    for listing in Section('oakland','sub', cachedir = None):
        print(listing)

Get the full text of the listing with the ``fulltext`` function. ::

    from craigsgenerator import Section
    for listing in Section('oakland','sub'):
        print(listing)
        print(fulltext(listing))
