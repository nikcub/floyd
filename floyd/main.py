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



# @TODO this can be a lot better
_TITLE_MATCH = re.compile('<h1 id="title">(.*)</h1>')

from optparse import OptionParser, NO_DEFAULT

parser = OptionParser(usage="%prog [options] <sources> <output>", prog=floyd.__clsname__, version="floyd v%s" % (floyd.__version__))
# parser = argparse.ArgumentParser(description='Static website generator for cloud hosting platforms', epilog='Report any issues to [Github url]')
parser.add_option('-s','--src', dest='src', type='string', default='sources', help='Project source ("src" by default)')
parser.add_option('-d','--dir', dest='out', type='string', default='site', help='The directory in which to create site (creates in "site" by default)')
parser.add_option('-t','--template', dest='template', type='string', default='default', help='Template to use (\'default\' by default)')
# @TODO
parser.add_option('-w','--watch', dest='out', type='string', default='site', help='Watch contents and automatically render and deploy')
# @TODO local server
# parser.add_option("--ignore-images", dest="ignore_images", action="store_true", default=False, help="don't include any formatting for images")
# parser.add_option("-g", "--google-doc", action="store_true", dest="google_doc", default=False, help="convert an html-exported Google Document")
# parser.add_option("-d", "--dash-unordered-list", action="store_true", dest="ul_style_dash", default=False, help="use a dash rather than a star for unordered list items")
        
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

def RenderPosts(posts, outputdir):  
  for post in posts:
    print 'rendering -- %s' % post.stub
    template_vars = {}
    template_vars['posts'] = posts[:5]
    template_vars['post'] = post
    template_vars = TemplateVars(template_vars)
    
    render = floyd.templating.jinja.render('single', template_vars)
    post_output_path = os.path.join(outputdir, post.stub)
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
  
    floyd.db.load_model_set(path_source)
    posts = floyd.db.query('posts')
    
    print "Got Posts:"
    print posts
    
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
  
  