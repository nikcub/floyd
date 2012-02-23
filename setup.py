#!/usr/bin/env python
import sys
import platform

if getattr(sys, 'version_info', (0, 0, 0)) < (2, 5, 0, 'final'):
    raise SystemExit("floyd requires Python 2.5 or later.")

from setuptools import setup
    
setup(
  name="floyd",
  description='Command line static website generator for cloud hosts',
  version='0.1',
  author='Nik Cubrilovic',
  author_email='nikcub@gmail.com',
  license='BSD 2-clause',
  packages=['floyd'],
  scripts=['bin/floyd'],
)