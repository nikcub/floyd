#!/usr/bin/env python
import sys
import os
import platform
import floyd

if getattr(sys, 'version_info', (0, 0, 0)) < (2, 5, 0, 'final'):
    raise SystemExit("floyd requires Python 2.5 or later.")

from setuptools import setup

scripts = ['bin/floyd']

if os.name == 'nt':
  scripts.append('bin/floyd.bat')

setup(
  name=floyd.__clsname__,
  description=floyd.__doc__.split('\n\n')[0],
  long_description=open('README.md').read(),
  keywords='website, appengine, s3, cms, blog',
  url=floyd.__url__,
  platforms=['linux', 'osx', 'win32'],
  version=floyd.__version__,
  author=floyd.__author__,
  author_email=floyd.__email__,
  license=floyd.__license__,
  install_requires=[
    'jinja2'
  ],
  packages=['floyd'],
  scripts=scripts,
)