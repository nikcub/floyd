#!/usr/bin/env python

"""Floyd
  
Datastore
"""

import os
import sys
import datetime

# register markdown extension dir
sys.path = sys.path + [os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'parsers'))]

import markdown

_MARKDOWN = markdown.Markdown(
  output_format='html4',
  extensions = ['footnotes', 'codehilite', 'microdata', 'headerid(forceid=False)', 'meta', 'time', 'floyd'],
  extension_configs= {'footnotes': [('PLACE_MARKER','++footnotes++')]},
)

_datastore = []

_DEFAULT_TYPEMAP = {
  'drafts': {
    'model': 'Post',
    'defaults': {
      'post_type': 'post',
      'post_status': 'draft'
    }
  },
  'pages': {
    'model': 'Post',
    'defaults': {
      'post_type': 'page',
      'post_status': 'published'
    }
  },
  'posts': {
    'model': 'Post',
    'defaults': {
      'post_type': 'post',
      'post_status': 'published'
    }
  },    
}

class DataStoreError(Exception):
  pass

class ModelAttributeError(Exception):
  pass

class DataStore(object):
  _model_cache = {}
  _store_cache = {}
  
  def __init__(self, datastore_path, type_map=None):
    """init new datastore"""
    self.datastore_path = datastore_path
    self.type_map = _DEFAULT_TYPEMAP
    
    if not os.path.isdir(self.datastore_path):
      raise DataStoreError('Not a valid datastore directory: %s' % self.datastore_path)
    
    for dirfile in os.listdir(self.datastore_path):
      if dirfile.startswith('_') or dirfile.startswith('.'):
        continue
      if not os.path.isdir(os.path.join(self.datastore_path, dirfile)):
        continue
      if dirfile in self.type_map:
        model_type = self.type_map[dirfile]
        full_path = os.path.realpath(os.path.join(self.datastore_path, dirfile))
        self.load_models_from_directory(full_path, **model_type)

  def import_model(self, name, path="floyd.db.models"):
    """imports a model of name from path, returning from local model
    cache if it has been previously loaded otherwise importing"""
    if name in self._model_cache:
      return self._model_cache[name]
  
    try:
      model = getattr(__import__(path, None, None, [name]), name)
      self._model_cache[name] = model
    except ImportError:
      return False
    return model

  def store_model(self, name, model):
    if not name in self._store_cache:
      self._store_cache[name] = []
    
    if not type(self._store_cache[name]) == type([]):
      raise Exception('Something went wrong')
    self._store_cache[name].append(model)

  def load_models_from_directory(self, path, model=None, defaults=None):
    print "Loading %s of type %s with %s" % (path, model, defaults)
    
    for modelfile in os.listdir(path):
      if modelfile.startswith('_') or modelfile.startswith('.'):
        continue
      if modelfile.endswith('.md'):
        m = self.import_model(model)(modelfile[:-3], **defaults)
        m.from_md_file(os.path.join(path, modelfile))
        self.store_model(model, m)

  def get_stored_models(self):
    return ', '.join(self._store_cache.keys())

  def get_models(self, model_type):
    if model_type.endswith('s'):
      model_type = model_type[:-1]
    if not model_type in self._store_cache:
      raise Exception('Model type not found: %s (have: %s)' % (model_type, self.get_stored_models()))
    return self._store_cache[model_type]

# @TODO model as dict
class Model(object):
  """Floyd base model class
  """
  __key__ = None
  post_type = None
  title = None
  stub = None
  
  def __init__(self, key, **kwargs):
    self.__key__ = key
    for k in kwargs:
      if hasattr(self, k):
        setattr(self, k, kwargs[k])
      else:
        raise ModelAttributeError('Model %s: Not a valid field %s' % (self.__class__, k))

  def from_md_file(self, path):
    print " model.from_md_file(%s)" % path
    self.raw_src = open(path).read()
    self.parse_md()

  def parse_md(self):
    """Takes a post path and returns a dictionary of variables"""
    post_content = _MARKDOWN.convert(self.raw_src)

    if hasattr(_MARKDOWN, 'Meta'):
      # 'Meta' in _MARKDOWN and _MARKDOWN.Meta:
      for key in _MARKDOWN.Meta:
        print "\t meta: %s: %s (%s)" % (key, _MARKDOWN.Meta[key][0], type(_MARKDOWN.Meta[key][0]))
        if key == 'pubdate':
          setattr(self, key, datetime.datetime.fromtimestamp(float(_MARKDOWN.Meta[key][0])))
        else:
          setattr(self, key, _MARKDOWN.Meta[key][0])
      
    self.content = post_content
    self.stub = self.__key__
  
    # set required fields
    # @TODO required in schema rather than here
    
    if not hasattr(self, 'pubdate'):
      print '\t Notice: setting default pubdate'
      setattr(self, 'pubdate', datetime.datetime.now())
  
    


class Query(object):
  
  def __init__(self, qs):
    """
      eg. t = Query('posts').filter(status='published').sort_by('-pubdate')
    """
    # print type(_datastore)
    self.model_type = qs
    self._dataset = _datastore.get_models(qs)

  def fetch(self, num=None):
    """fetch results from dataset
    """
    if num:
      return self._dataset[:num]
    else:
      return self._dataset
  
  def filter(self, **kwargs):
    # @TODO refactor with models as dicts
    """filter results of dataset eg.
    
    Query('Posts').filter(post_type='post')
    """
    f_field = kwargs.keys()[0]
    f_value = kwargs[f_field]
    _newset = []
    
    for m in self._dataset:
      if hasattr(m, f_field):
        if getattr(m, f_field) == f_value:
          _newset.append(m)
    self._dataset = _newset
    return self

  def sort_by(self, sb):
    """Sort results"""
    
    return self.sort(key=lambda x: x.pubdate, reverse=True)
    
  def __len__(self):
    return len(self._dataset)


def setup(datastore_path):
  global _datastore
  _datastore = DataStore(datastore_path)
