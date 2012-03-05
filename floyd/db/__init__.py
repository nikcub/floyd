#!/usr/bin/env python

"""Floyd
  
Module entry point
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

__posts = []

class Model(object):
  """Floyd base model class
  """

  def from_md_file(self, key, path):
    print " model.from_md_file(%s)" % path
    self.__key__ = key
    self.raw_src = open(path).read()
    self.parse()

  def parse(self):
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
    
    if not hasattr(self, 'pubdate'):
      print '\t Notice: setting default pubdate'
      setattr(self, 'pubdate', datetime.datetime.now())
  
    


class Post(Model):
  pass


def query(q):
  global __posts
  return __posts

def load_model_set(path):
  if not os.path.isdir(path):
    raise Exception('No a valid model source directory: %s' % path)
  
  for dirfile in os.listdir(path):
    if dirfile.startswith('_') or dirfile.startswith('.'):
      continue
    if os.path.isdir(os.path.join(path, dirfile)):
      load_models_from_directory(os.path.join(path, dirfile), post_type=dirfile)

def load_models_from_directory(path, post_type):
  print "Loading %s from %s" % (post_type, path)
  
  for modelfile in os.listdir(path):
    if modelfile.startswith('_') or modelfile.startswith('.'):
      continue
    if modelfile.endswith('.md'):
      m = Post()
      m.from_md_file(modelfile[:-3], os.path.join(path, modelfile))
      __posts.append(m)


#---------------------------------------------------------------------------
#   unused
#---------------------------------------------------------------------------


def GetPosts(path):
  if not os.path.isdir(path):
    raise Exception('Not a valid posts directory: %s' % path)
  
  posts = []
  for postfile in os.listdir(path):
    if postfile.startswith('.'):
      continue
    if postfile.endswith('.md'):
      post = ParsePost(os.path.join(path, postfile), postfile)
      if post:
        posts.append(post)
  return posts

def load_models_from_directory_old(sources_dir):
  data_files = []
  packages = []
  for dirpath, dirnames, filenames in os.walk(sources_dir):
    print 'walking: %s - %s - %s' % (dirpath, dirnames, filenames)
    for i, dirname in enumerate(dirnames):
      if dirname.startswith('.'): 
        del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(floyd.util.path.split(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
