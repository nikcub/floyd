#!/usr/bin/env python

"""path utilities
"""

import os

def split(path, result=None):
  """
  Split a pathname into components (the opposite of os.path.join) in a
  platform-neutral way.
  """
  if result is None:
    result = []
  head, tail = os.path.split(path)
  if head == '':
    return [tail] + result
  if head == path:
    return result
  return split(head, [tail] + result)