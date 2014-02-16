from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='craigsgenerator',
    author='Thomas Levine',
    author_email='_@thomaslevine.com',
    description='Iterate through Craig\'s list',
    long_description=long_description,
    url='https://github.com/tlevine/craigsgenerator.git',
    classifiers=[
        'Intended Audience :: Developers',
    ],
    packages=['craigsgenerator'],

    install_requires = ['nosetests','lxml'],

    version=craigsgenerator.__version__,
    license='MIT'
)
