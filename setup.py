#!/usr/bin/env python

from setuptools import setup

pyuntl_url = 'git+https://github.com/unt-libraries/pyuntl.git@master#egg=pyuntl'

setup(
    name='m2m',
    version='2.0.0',
    url='https://github.com/unt-libraries/m2m',
    author='Mark Phillips',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    packages=['m2m'],
    scripts=['m2m/m2m.py'],
    install_requires=['pyuntl @' + pyuntl_url],
    dependency_links=[pyuntl_url],
    description='Package and command line tool for mapping csv files to UNTL metadata records.',
    long_description='See the home page for more information.',
    classifiers=[
        'Intended Audience :: Education'
        'Intended Audience :: Developers'
        'Intended Audience :: Information Technology'
        'License :: OSI Approved :: BSD License'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
)
