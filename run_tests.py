#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, call

def patch_path():
  cur_dirname = os.path.dirname(__file__)
  if not cur_dirname in sys.path:
    sys.path.insert(0, cur_dirname)
  
if __name__ == '__main__':
  patch_path()
  call(["python", "./floyd/tests/__init__.py"])
