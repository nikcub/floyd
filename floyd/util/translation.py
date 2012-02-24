#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:expandtab
#
# Copyright (c) 2011, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#
"""
  floyd - util - translation.py

  desc

  @TODO support translations with Babel module
  see: http://stackoverflow.com/questions/3821312/gae-webapp-application-internationalization-with-babel
  see: http://babel.edgewall.org/
"""
from .unicode import force_unicode

def ugettext(str, format=unicode):
  return force_unicode(str)

def ngettext(singular, plural, number):
  if number == 1: return singular
  return plural

def ungettext(singular, plural, number):
  return force_unicode(ngettext(singular, plural, number))
