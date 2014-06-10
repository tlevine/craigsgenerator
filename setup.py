from distutils.core import setup

install_requires = ['requests','lxml','python-dateutil']
if sys.version[0] == '2':
    install_requires.append('futures')

setup(name='craigsgenerator',
    author='Thomas Levine',
    author_email='_@thomaslevine.com',
    description='Iterate through Craig\'s list',
    url='https://github.com/tlevine/craigsgenerator.git',
    classifiers=[
        'Intended Audience :: Developers',
    ],
    packages=['craigsgenerator'],
    install_requires = install_requires,
    tests_require = ['nose'],
    version='0.1.1',
    license='AGPL'
)
