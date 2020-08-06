#!/usr/bin/env python3
from os.path import dirname, join
from setuptools import setup, find_packages


setup(
    name='FetchCord',
    version=0.1,
    description='grabs information about your Distro and displays it as Discord Rich Presence.',
    long_description=open(
        join(dirname(__file__), 'readme.md')).read(),
    url='https://github.com/MrPotatoBobx/FetchCord',
    author='MrPotatoBobx',
    author_email='',
    license='MIT',
    packages=['fetch_cord'],
    keywords=['distro', 'info', 'discord', 'fetch'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

