#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='bash_concurrent',
    description='Wrapper around the bash-concurrent bash library',
    url='https://github.com/gdraynz/py-bash-concurrent',
    author='gdraynz',
    author_email='gdraynz@gmail.com',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
)
