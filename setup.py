#!/usr/bin/env python

import os
import re
import sys

from codecs import open

try:
    from setuptools import find_packages
    from setuptools import setup
except ImportError:
    from distutils.core import find_packages
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

version = ''
with open('webest/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()
with open('requirements.txt', 'r', 'utf-8') as f:
    requires = [s.strip() for s in f.read().splitlines()]

setup(
    name='webest',
    version=version,
    description='Easier Web Automation',
    long_description=readme + '\n\n' + history,
    author='Alvaro Lopez Ortega',
    author_email='alvaro@alobbs.com',
    url='https://github.com/alobbs/webest',
    install_requires=requires,
    packages=find_packages(),
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
