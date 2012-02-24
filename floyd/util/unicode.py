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
  floyd - unicode.py
  
  unicode and text tools

"""


def force_unicode(text, encoding='utf-8'):
  """
  
  @TODO encoding support
  """
  if text == None:
    return u''

  try:
    text = unicode(text, 'utf-8')
  except UnicodeDecodeError:
    text = unicode(text, 'latin1')
  except TypeError:
    text = unicode(text)
  return text

def force_utf8(text):
  return str(force_unicode(text).encode('utf8'))
    


def to_utf8(value):
  """Returns a string encoded using UTF-8.

  This function comes from `Tornado`_.

  :param value:
    A unicode or string to be encoded.
  :returns:
    The encoded string.
  """
  if isinstance(value, unicode):
    return value.encode('utf-8')

  assert isinstance(value, str)
  return value


def to_unicode(value):
  """Returns a unicode string from a string, using UTF-8 to decode if needed.

  This function comes from `Tornado`_.

  :param value:
    A unicode or string to be decoded.
  :returns:
    The decoded string.
  """
  if isinstance(value, str):
    return value.decode('utf-8')

  assert isinstance(value, unicode)
  return value

