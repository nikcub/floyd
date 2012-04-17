#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import platform
import floyd


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


if getattr(sys, 'version_info', (0, 0, 0)) < (2, 5, 0, 'final'):
    raise SystemExit("floyd requires Python 2.5 or later.")

if sys.argv[-1] == 'publish':
  os.system('python setup.py sdist upload')
  sys.exit()

if sys.argv[-1] == 'test':
  os.system('python test_floyd.py')
  sys.exit()

scripts = ['bin/floyd']
packages = [
  'jinja2',
  'markdown',
  'yaml'
]

if os.name == 'nt':
  scripts.append('bin/floyd.bat')

def get_file_contents(file_path, curfile=__file__ or ''):
  """Get the context of the file using full path name"""
  try:
    full_path = os.path.join(os.path.realpath(os.path.dirname(curfile)), 
                             file_path)
    return open(full_path, 'r').read()
  except (IOError, NameError, TypeError):
    return ""

setup(
  name = 'floyd',
  description = floyd.__doc__.split('\n\n')[0],
  long_description = get_file_contents('README.md'),
  keywords = 'website, appengine, s3, cms, blog',
  url = floyd.__url__,
  platforms = ['linux', 'osx', 'win32'],
  version = floyd.__version__,
  author = floyd.__author__,
  author_email = floyd.__email__,
  license = floyd.__license__,
  install_requires = packages,
  packages = ['floyd'],
  scripts = scripts,
)