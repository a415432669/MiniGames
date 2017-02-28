#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__author__ = 'fyabc'

setup(
    name='HearthStone',
    version='1.0',
    keywords=('HearthStone', 'game'),
    description='A Python implementation of HearthStone.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/HearthStone',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'hearthstone = HearthStone.main:main',
        ]
    },
)
