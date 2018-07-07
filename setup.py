#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Testing',
]

setup(
    name='pure-python-adb',
    version="0.1.5-dev",
    description='Pure python implementation of the adb client',
    long_description=readme + '\n\n' + history,
    author='Swind Ou',
    author_email='swind@cloudmosa.com',
    url="https://github.com/Swind/pure-python-adb",
    license='MIT license',
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    install_requires=[],
    keywords="adb",
    classifiers=classifiers,
)
