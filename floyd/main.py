#!/usr/bin/env python
#
# Copyright (c) 2010-2012, Nik Cubrilovic 
# <nikcub@gmail.com> <http://nikcub.appspot.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
# 
#   2.  Redistributions in binary form must reproduce the above copyright notice, 
#       this list of conditions and the following disclaimer in the documentation 
#       and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR CONTRIBUTORS BE LIABLE FOR 
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import sys
import re
import getopt
import logging
import datetime
import yaml
import floyd
import markdown

from .templating import jinja

logging.basicConfig(level=logging.INFO)

ARG_SOURCE_DIR = 'source'
ARG_OUTPUT_DIR = 'ouput'

DEFAULT_ARGS = {
  ARG_SOURCE_DIR: 'sources',
  ARG_OUTPUT_DIR: 'site',
}

# register markdown extension dir
sys.path = sys.path + [os.path.join(os.path.dirname(__file__), 'parsers')]

_MARKDOWN = markdown.Markdown(
  output_format='html4',
  extensions = ['footnotes', 'codehilite', 'microdata', 'headerid(forceid=False)', 'meta', 'time', 'floyd'],
  extension_configs= {'footnotes': [('PLACE_MARKER','++footnotes++')]},
)

# @TODO this can be a lot better
_TITLE_MATCH = re.compile('<h1 id="title">(.*)</h1>')

from optparse import OptionParser, NO_DEFAULT

parser = OptionParser(usage="%prog [options] <sources> <output>", prog=floyd.__clsname__, version="floyd v%s" % (floyd.__version__))
# parser = argparse.ArgumentParser(description='Static website generator for cloud hosting platforms', epilog='Report any issues to [Github url]')
parser.add_option('-s','--src', dest='src', type='string', default='sources', help='Project source ("src" by default)')
parser.add_option('-d','--dir', dest='out', type='string', default='site', help='The directory in which to create site (creates in "site" by default)')
# @TODO
parser.add_option('-w','--watch', dest='out', type='string', default='site', help='Watch contents and automatically render and deploy')
# @TODO local server

def ParseArguments(argv):
  user_options = DEFAULT_ARGS.copy()

def PrintUsageExit(code=-1):
  render_dict = DEFAULT_ARGS.copy()
  render_dict['script'] = floyd.__clsname__
  print sys.modules['__main__'].__doc__ % render_dict
  sys.stdout.flush()
  sys.exit(code)

def TemplateVars(vars):
  additional = {
    'admin': False,
    'user': None,
    'logout': '/',
    'login': '/',
    'static_host': 'sketch-proto.appspot.com',
    'css_file': 'nikcub.030.min.css',
    'css_ver': '26',
    'src': 'database',
  }
  return dict(zip(additional.keys() + vars.keys(), additional.values() + vars.values()))
  
def ParsePost(path, name):
  """Takes a post path and returns a dictionary of variables"""
  if not os.path.isfile(path):
    return None
  
  print "Parsing: %s" % name
  
  post = {}
  fh = open(path, 'r')
  fc = fh.read()
  
  try:
    post_content = _MARKDOWN.convert(fc)
  except Exception, e:
    print '  - markdown error: %s' % str(e)

  if _MARKDOWN.Meta:
    for key in _MARKDOWN.Meta:
      print "\t meta: %s: %s (%s)" % (key, _MARKDOWN.Meta[key][0], type(_MARKDOWN.Meta[key][0]))
      if key == 'pubdate':
        post[key] = datetime.datetime.fromtimestamp(float(_MARKDOWN.Meta[key][0]))
      else:
        post[key] = _MARKDOWN.Meta[key][0]
      
  post['content'] = post_content
  post['stub'] = name.split('.')[0]
  
  if not 'pubdate' in post:
    print '  - setting default pubdate'
    post['pubdate'] = datetime.datetime.now()
  
  # print "Parsed %s output:" % (name)
  # for key in post:
  #   print "\t %s: %s" % (key, post[key])

  return post

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

def FindModels(sources_dir):
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


def RenderPosts(posts, outputdir):  
  for post in posts:
    print 'rendering -- %s' % post['stub']
    template_vars = {}
    template_vars['posts'] = posts[:5]
    template_vars['post'] = post
    template_vars = TemplateVars(template_vars)
    
    render = jinja.render('single', template_vars)
    post_output_path = os.path.join(outputdir, post['stub'])
    print 'render: %s ' % post_output_path
    fp = open(post_output_path, 'w')
    fp.write(render)
    fp.close()
    
def Main(argv):
  (options, args) = parser.parse_args()
  curdir = os.getcwd()
  try:
    path_source = os.path.join(curdir, options.src)
    path_output = os.path.join(curdir, options.out)
    path_templates = os.path.join(path_source, 'templates', 'default')
    
    if not os.path.isdir(path_source):
      parser.error('Not a valid source directory: %s' % path_source)
    if not os.path.isdir(path_output):
      parser.error('Not a valid output directory: %s' % path_output)
    if not os.path.isdir(path_templates):
      parser.error('Not a valid template directory: %s' % path_templates)

    jinja.setup(path_templates)
  
    # FindModels(path_source)

    posts = GetPosts(os.path.join(path_source, 'posts'))
    RenderPosts(posts, path_output)
    
  except ArgumentError as (errno, strerror):
    print "Error: %s" % strerror
    return -1



class ArgumentError(Exception):
  pass

if __name__ == '__main__':
  print sys.argv
  sys.exit(Main(sys.argv))
  
  