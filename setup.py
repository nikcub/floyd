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

scripts = ['floyd/bin/floyd']
packages = [
  'jinja2',
  'markdown'
]

if os.name == 'nt':
  scripts.append('floyd/bin/floyd.bat')

package_dir = os.path.realpath(os.path.dirname(__file__))

def get_file_contents(file_path):
  """Get the context of the file using full path name"""
  full_path = os.path.join(package_dir, file_path)
  return open(full_path, 'r').read()

setup(
  name = 'floyd',
  description = floyd.__doc__.split('\n\n')[0],
  long_description = get_file_contents('README.md'),
  keywords = 'website, appengine, s3, cms, blog',
  url = floyd.__url__,
  platforms = ['linux', 'osx', 'win32'],
  version = floyd.get_version(),
  author = floyd.__author__,
  author_email = floyd.__email__,
  license = get_file_contents('LICENSE'),
  install_requires = packages,
  packages = ['floyd'],
  scripts = scripts,
)