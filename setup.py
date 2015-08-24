#!/usr/bin/env python

from setuptools import setup

setup(
    name='m2m',
    version='1.0.0',
    url='https://github.com/unt-libraries/m2m',
    author='Mark Phillips',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    packages=['m2m'],
    scripts=['m2m/m2m.py'],
    install_requires=['pyuntl'],
    description='Module and command line tool for mapping csv files to UNTL metadata records.',
    long_description='See the home page for more information.',
    classifiers=[
        'Intended Audience :: Education'
        'Intended Audience :: Developers'
        'Intended Audience :: Information Technology'
        'License :: OSI Approved :: BSD License'
        'Programming Language :: Python'
    ],
    test_suite='tests',
)
