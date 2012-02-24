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
import getopt
import logging

import floyd

from .templating import jinja

logging.basicConfig(level=logging.INFO)

ARG_SOURCE_DIR = 'source'
ARG_OUTPUT_DIR = 'ouput'

DEFAULT_ARGS = {
  ARG_SOURCE_DIR: 'sources',
  ARG_OUTPUT_DIR: 'site',
}


from optparse import OptionParser

parser = OptionParser(usage="%prog [options] <sources> <output>", prog=floyd.__clsname__, version="floyd v%s" % (floyd.__version__))
# parser = argparse.ArgumentParser(description='Static website generator for cloud hosting platforms', epilog='Report any issues to [Github url]')
parser.add_option('-s','--src', dest='src', type='string', default='sources', help='Project source ("src" by default)')
parser.add_option('-d','--dir', dest='out', type='string', default='site', help='The directory in which to create site (creates in "site" by default)')

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
  
def ParsePost(path):
  """Takes a post path and returns a dictionary of variables"""
  import datetime
  post_vars = {}
  post = {
    'title': 'post title',
    'content': 'post content',
    'pubdate': datetime.datetime.now()
  }
  post_vars['post'] = post
  return TemplateVars(post_vars)

def Main(argv):
  (options, args) = parser.parse_args()
  curdir = os.getcwd()
  try:
    path_source = os.path.join(curdir, options.src)
    path_output = os.path.join(curdir, options.out)
    path_templates = os.path.join(path_source, 'templates')
    example_post = os.path.join(path_source, 'posts', 'test-post')
    example_output = os.path.join(path_output, 'test-post.html')
    
    if not os.path.isdir(path_source):
      parser.error('Not a valid source directory: %s' % path_source)
    if not os.path.isdir(path_output):
      parser.error('Not a valid output directory: %s' % path_output)
      
    if not os.path.isdir(path_templates):
      parser.error('Not a valid template directory: %s' % path_templates)
    if not os.path.isfile(example_post):
      parser.error('Not a valid blog post')
    
  except IOError as (errno, strerror):
    print "Error"
    return -1
  except Exception as errstr:
    print "Error: %s" % errstr
    return -1
  
      
  template_sets = {'site': path_templates}
  jinja.setup(template_sets)
  
  post_vars = ParsePost(example_post)
  render = jinja.render('single', post_vars, 'site', 'default')
  fp = open(example_output, 'w')
  fp.write(render)
  fp.close()

if __name__ == '__main__':
  print sys.argv
  sys.exit(Main(sys.argv))
  
  