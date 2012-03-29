import sys

class ConstError(TypeError): pass

class _const:
  def __setattr__(self, name, value):
    if self.__dict__.has_key(name):
      raise self.ConstError, "Can't rebind const(%s)" % name
    self.__dict__[name]=value

sys.modules[__name__]=_const()