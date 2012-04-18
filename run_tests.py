#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def patch_path():
  cur_dirname = os.path.dirname(__file__)
  if not cur_dirname in sys.path:
    sys.path.insert(0, cur_dirname)
  
if __name__ == '__main__':
  patch_path()
  import floyd
  floyd.tests.main()
