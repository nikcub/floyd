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

import floyd.db
import floyd.templating.jinja

logging.basicConfig(level=logging.INFO)

ARG_SOURCE_DIR = 'source'
ARG_OUTPUT_DIR = 'ouput'

DEFAULT_ARGS = {
  ARG_SOURCE_DIR: 'sources',
  ARG_OUTPUT_DIR: 'site',
}


_DEFAULT_ROUTES = [
  ('/', 'controllers.index'),
  ('/archive', 'controllers.archive'),
  ('/<stub>', 'controllers.page'),
  ('/posts/<stub>', 'controllers.post')
]

# @TODO this can be a lot better
_TITLE_MATCH = re.compile('<h1 id="title">(.*)</h1>')

from optparse import OptionParser, NO_DEFAULT

parser = OptionParser(usage="%prog [options]", prog=floyd.__clsname__, version="floyd v%s" % (floyd.__version__))
# parser = argparse.ArgumentParser(description='Static website generator for cloud hosting platforms', epilog='Report any issues to [Github url]')
parser.add_option('-s','--src', dest='src', type='string', default='sources', help='Project source ("src" by default)')
parser.add_option('-d','--dir', dest='out', type='string', default='site', help='The directory in which to create site (creates in "site" by default)')
parser.add_option('-t','--template', dest='template', type='string', default='default', help='Template to use (\'default\' by default)')
parser.add_option('-p', dest='pyfile', type='string', default='', help='read config from python file')
# @TODO watcher
# parser.add_option('-w','--watch', dest='out', type='string', default='site', help='Watch contents and automatically render and deploy')
# @TODO local server
# parser.add_option('-s', '--server', dest='server', action='store_true', default=False, help='server')

def Main(argv):
  (options, args) = parser.parse_args()
  curdir = os.getcwd()
  try:
    path_source = os.path.join(curdir, options.src)
    path_output = os.path.join(curdir, options.out)
    path_templates = os.path.join(curdir, 'templates')
    template_name = options.template
    path_template = os.path.join(path_templates, template_name)
    
    if not os.path.isdir(path_source):
      parser.error('Not a valid source directory: %s' % path_source)
    if not os.path.isdir(path_output):
      parser.error('Not a valid output directory: %s' % path_output)
    if not os.path.isdir(path_template):
      parser.error('Not a valid template directory or template: %s' % path_templates)

    floyd.templating.jinja.setup(path_template)
    floyd.db.setup(path_source)

    posts = floyd.db.Query('Posts').filter(post_type='post').filter(post_status='published').fetch(100)
    drafts = floyd.db.Query('Posts').filter(post_type='post').filter(post_status='draft').fetch(100)
    pages = floyd.db.Query('Posts').filter(post_type='page').fetch(100)

    
    print "\nGot drafts: (%d)" % len(drafts)
    for p in drafts:
      print "%s - %s - %s"% (p.__key__, p.stub, p.title)
          
    print "\nGot Posts: (%d)" % len(posts)
    for p in posts:
      print "%s - %s - %s"% (p.__key__, p.stub, p.title)
    
    print "\nGot Pages: (%d)" % len(pages)
    for p in pages:
      print "%s - %s - %s" % (p.__key__, p.stub, p.title)
    
    # posts = GetPosts(os.path.join(path_source, 'posts'))
    RenderPosts(posts, path_output)
    
  except ArgumentError as (errno, strerror):
    print "Error: %s" % strerror
    return -1



class ArgumentError(Exception):
  pass

if __name__ == '__main__':
  print sys.argv
  sys.exit(Main(sys.argv))
  
  