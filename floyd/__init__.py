#!/usr/bin/env python

"""A command line static website generator for popular cloud hosting providers

:copyright: Copyright (C) 2012 Nik Cubrilovic and others, see AUTHORS
:license: new BSD, see LICENSE for more details.

"""

import sys
from floyd.core.command_utils import run_cl

VERSION = (0, 0, 3, 'alpha', 11)

__clsname__ = 'floyd'
__author__ = 'Nik Cubrilovic <nikcub@gmail.com>'
__email__ = 'nikcub@gmail.com'
__url__ = 'http://github.com/nikcub/floyd'
__license__ = 'BSD'
__copyright__ = 'Copyright (c) 2012, Nik Cubrilovic. All rights reserved.'


def get_version(version=None):
  if version is None:
    version = VERSION
  assert version[3] in ('alpha', 'beta', 'rc', 'final')
  parts = 2 if version[2] == 0 else 3
  main = '.'.join(str(x) for x in version[:parts])
  sub = ''
  if version[3] != 'final':
    mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
    sub = mapping[version[3]] + str(version[4])
  return main + sub

if __name__ == '__main__':
  sys.exit(run_cl())

