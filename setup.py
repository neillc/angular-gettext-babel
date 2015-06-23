"""A setuptools based setup module for babel-angular-gettext
Based on:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='angular-gettext-babel',
    version='0.1',
    description='A plugin for babel to work with angular-gettext templates',
    long_description=read('README.rst') + u'\n\n' + read('CHANGELOG.rst'),
    url='https://github.com/neillc/angular-gettext-babel',
    author='Neill Cox',
    author_email='neill@ingenious.com.au',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Internationalisation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='angular-gettext babel',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['babel'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={},
    data_files=[],
    entry_points={
        'babel.extractors': [
            'angulargettext=angulargettext.extract:extract_angular_gettext',
        ],
    },
)