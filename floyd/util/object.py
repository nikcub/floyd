#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:expandtab
#
# Copyright (c) 2010-2011, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#


#---------------------------------------------------------------------------
#   Python Object Oriented Helper Functions
#---------------------------------------------------------------------------

def hasmethod(obj, meth):
  """
    Checks if an object, obj, has a callable method, meth
    
    return True or False
  """
  if hasattr(obj, meth):
    return callable(getattr(obj,meth))
  return False

def hasvar(obj, var):
  """
    Checks if object, obj has a variable var
    
    return True or False
  """
  if hasattr(obj, var):
    return not callable(getattr(obj, var))
  return False

def getmethattr(obj, meth):
  """
    Returns either the variable value or method invocation
  """
  if hasmethod(obj, meth):
    return getattr(obj, meth)()
  elif hasvar(obj, meth):
    return getattr(obj, meth)
  return None


def assure_obj_child_dict(obj, var):
  """Assure the object has the specified child dict
  """
  if not var in obj or type(obj[var]) != type({}):
    obj[var] = {}
  return obj
  

class Bunch(dict):
  def __init__(self, **kw):
    dict.__init__(self, kw)
    self.__dict__.update(kw)
        
class AccessibleDict(dict):
  dirty = True

  def __repr__(self): 
    return repr(self.data)
    
  def __len__(self): return len(self.data)
  def clear(self): self.data.clear()
  def copy(self): return self.data.copy()
  def keys(self): return self.data.keys()
  def items(self): return self.data.items()
  def iteritems(self): return self.data.iteritems()
  def iterkeys(self): return self.data.iterkeys()
  def itervalues(self): return self.data.itervalues()
  def values(self): return self.data.values()
  def has_key(self, key): return key in self.data

  def get(self, key, default = None):
    if key not in self.data:
      return default
    return self[key]

  def __str__(self):
    return str(self.data)

  def __delitem__(self, key):
    del self.data[key]
    self.dirty = True

  def __getitem__(self, key):
    if key in self.data:
      return self.data[key]
    raise KeyError(key)

  def __setitem__(self, key, val):
    if type(val) is dict:
      val = AccessibleDict(val)
    self.data[key] = val
    self.dirty = True

  def __getattr__(self, key):
    return self.get(key)

  def __contains__(self, key):
    return key in self.data

  def __iter__(self):
    return iter(self.data)


class AttrDict(dict):
  """Smart Dict
  
  * get elements as attributes
  * marked as dirty when not saved
  * will persist all dict values as attrdicts as well 
  
  @TODO implement 'dirty chain' (ie. mark parent as dirty)
  @TODO see http://code.google.com/p/pycopia/source/browse/trunk/aid/pycopia/dictlib.py
  """
  __dirty__ = False
  
  def __init__(self, *args, **kwargs):
    self.__dirty__ = True
    dict.__init__(self, *args, **kwargs)

  def __getattr__(self, attr):
    """
    
    :raises AttributeError:
    """
    return dict.__getitem__(self, attr)

  def __setattr__(self, attr, value):
    if attr.startswith('__'):
      self.__dict__[attr] = value
      return None
    self.__setitem__(attr, value)

  def __delattr__(self, name):
    # self.__dirty__ = True
    return dict.__delattr__(self, name)

  
  def __setitem__(self, key, val):
    if type(val) is dict:
      val = AttrDict(val)
    dict.__setitem__(self, key, val)
    self.__dirty__ = True
  
  @property
  def dirty():
    return self.__dirty__

class RecursiveDict(dict):
  """Implementation of perl's autovivification feature."""
  def __missing__(self, key):
    value = self[key] = type(self)()
    return value
  
from keyword import iskeyword 

def checkattr(attr):
  if not attr.isalnum():
    raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
  if iskeyword(name):
    raise ValueError('Type names and field names cannot be a keyword: %r' % name)
  if name[0].isdigit():
    raise ValueError('Type names and field names cannot start with a number: %r' % name)

if __name__ == '__main__':
  t = AttrDict(first = 'one', second = 'two')
  print t
  t.third = 'three'
  print t
  t['fourth'] = 'four'
  print t
  t.fifth = {'fifth': 'dict test'}
  print t
  print t.get('no')
  # t.fifth = {'five': 'dict'}
  # print t
  # print t.keys()
  # for k in t:
  #   print "> %s => %s" % (k, getattr(t, k))
  
  
  