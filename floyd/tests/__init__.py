#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#
""" Floyd tests
  
"""

import os
import sys
import floyd
import unittest

class CommandlineTests(unittest.TestCase):
  def test_cl_no_options(self):
    test_argv = []
    app = floyd.core.command_utils.run_cl(test_argv)
    self.assertEquals(app, 2)
  
  def test_cl_invalid_option(self):
    test_argv = ['floyd', '-invalid_argument']
    app = floyd.core.command_utils.run_cl(test_argv)
    self.assertEquals(app, 2)

  def test_cl_invalid_subcommand(self):
    test_argv = ['floyd', '_invalid_command']
    app = floyd.core.command_utils.run_cl(test_argv)
    self.assertEquals(app, 2)

class DefaultTests(unittest.TestCase):
  def setup(self):
    cl_arg = 'whereis floyd'

  def test_cl_no_options(self):
    test_argv = []
    app = floyd.core.command_utils.run_cl(test_argv)
    self.assertEquals(app, 2)
  
  def test_cl_invalid_option(self):
    test_argv = ['floyd', '-invalid_argument']
    app = floyd.core.command_utils.run_cl(test_argv)
    self.assertEquals(app, 2)

  def test_cl_invalid_subcommand(self):
    test_argv = ['floyd', '_invalid_command']
    app = floyd.core.command_utils.run_cl(test_argv)
    self.assertEquals(app, 2)
  
def mksuite(test_class):
  return unittest.makeSuite(test_class)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTests((mksuite(CommandlineTests), mksuite(DefaultTests)))
  return suite

def main():
  unittest.main(defaultTest='test_suite')

if __name__ == '__main__': 
  unittest.main(defaultTest='test_suite')