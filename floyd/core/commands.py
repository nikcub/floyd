#!/usr/bin/env python
#
# Copyright (c) 2012, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#
"""Floyd commands

The first argument is the command line options and the remaining function arguments
are command line arguments as defined in the parser

On a command error throw CommandError with a detailed description. This will refer
the user to the help page

"""

import os
import sys
import floyd.db
import floyd.templating.jinja
import floyd.controllers

from floyd.core.multiopt import CommandError

def init(options, init_type=None, path='.'):
  valid_inits = ['gae', 's3']
  if not init_type in valid_inits:
    raise CommandError("Type must be one of %s" % (", ".join(valid_inits)))
  curdir = os.path.realpath(os.getcwd())
  path_init = os.path.realpath(os.path.join(curdir, path))
  
  if not os.path.isdir(path_init):
    raise CommandError("Not a valid init directory: %s" % path_init)
    
  print 'init command run.. %s' % path_init
  # mkdir('sources')
  # mkdir('sources', 'posts')
  # mkdir('sources', 'pages')
  # mkdir('site')
  # mkdir('templates')
  # touch('robots.txt')
  # touch('favicon.ico')
  return 1


def generate(options, source='sources', dest='site'):  
  curdir = os.getcwd()
  path_source = os.path.join(curdir, source)
  path_output = os.path.join(curdir, dest)
  path_templates = os.path.join(curdir, 'templates')
  template_name = options.template
  path_template = os.path.join(path_templates, template_name)

  if not os.path.isdir(path_source):
    raise CommandError('Not a valid source directory: %s' % path_source)
  if not os.path.isdir(path_output):
    raise CommandError('Not a valid output directory: %s' % path_output)
  if not os.path.isdir(path_template):
    raise CommandError('Not a valid template directory or template: %s' % path_templates)

  floyd.templating.jinja.setup(path_template)
  floyd.db.setup(path_source)

  posts = floyd.db.Query('Posts').filter(post_type='post').filter(post_status='published').fetch(100)
  drafts = floyd.db.Query('Posts').filter(post_type='post').filter(post_status='draft').fetch(100)
  pages = floyd.db.Query('Posts').filter(post_type='page').fetch(100)

def deploy(options):
  print 'help command run..'
  return 1

def serve(options):
  print 'help command run..'
  return 1

def watch(options):
  print 'help command run..'
  return 1

def create_site():

  pass