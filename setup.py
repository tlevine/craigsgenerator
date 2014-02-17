from distutils.core import setup

def read(fn):
    with open(fn) as file:
        out = file.read()
    return out

setup(name='craigsgenerator',
    author='Thomas Levine',
    author_email='_@thomaslevine.com',
    description='Iterate through Craig\'s list',
    long_description = read('README.rst'),
    url='https://github.com/tlevine/craigsgenerator.git',
    classifiers=[
        'Intended Audience :: Developers',
    ],
    packages=['craigsgenerator'],

    install_requires = ['requests','lxml'],
    tests_require = ['nose'],

    version='0.0.10',
    license='AGPL'
)
