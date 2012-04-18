#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, Nik Cubrilovic. All rights reserved.
#
# <nikcub@gmail.com> <http://nikcub.appspot.com>  
#
# Licensed under a BSD license. You may obtain a copy of the License at
#
#     http://nikcub.appspot.com/bsd-license
#
""" floyd - command_utils.py

Default command line utitlities to run floyd

@TODO need to really improve the long helps
"""

import os
import sys
import logging

import floyd.core.commands
from floyd.core.multiopt import MultioptParser, SubCommand, make_option



_DEFAULT_ROUTES = [
  ('/', 'controllers.index'),
  ('/archive', 'controllers.archive'),
  ('/<stub>', 'controllers.page'),
  ('/posts/<stub>', 'controllers.post')
]

_DEFAULT_GENERATOR = [
  # (post.stub in floyd.db.Query('Posts').filter(post_type='post').filter(post_status='published').fetch(100))
  # map(post, posts)
  # or list expression
  # [controllers.post(p, '/posts/<stub>') for p in posts]
]
# @TODO this can be a lot better
# _TITLE_MATCH = re.compile('<h1 id="title">(.*)</h1>')


commands = {

  'init': SubCommand(
    func=floyd.core.commands.init,
    usage='%prog init [options] <type> [directory]',
    desc_short='Initialize a new site directory',
    desc_long="""Generates a new site with a template in directory
specified by <directory> or by default in the
current directory

'type' must be one of 'gae' for AppEngine or 's3' for Amazon S3""",
    options=[
    ]
  ),

  'generate': SubCommand(
    func=floyd.core.commands.generate,
    usage='%prog [options] generate <source> <destination>',
    desc_short='Generate site or page from source into destination',
    desc_long="""Generate a single page from markdown source 'README.md' to HTML page 'README.html':

  $ floyd generate README.md README.html

Generate from a site directory with config to an output directory using template 'default'

  $ floyd generate -t default sources/ site/
""",
    options=[
      make_option('-t', '--template', action="store", default='default', type="string", dest="template"),
    ]),

  'deploy': SubCommand(
    func=floyd.core.commands.deploy,
    usage='%prog [options] deploy <directory>',
    desc_short='Deploy a site',
    desc_long="""""",
    options=[
    ]),

  # 'serve': SubCommand(
  #   func=floyd.core.commands.serve,
  #   usage='%prog [options] serve <directory>',
  #   desc_short='Run local server instance',
  #   desc_long="""""",
  #   options=[
  #   ]),
  # 
  # 'watch': SubCommand(
  #   func=floyd.core.commands.watch,
  #   usage='%prog [options] watch <directory>',
  #   desc_short='Watch site and auto-deploy on publish',
  #   options=[
  #     make_option('-S', action="store_true", dest="onsave", help="deploy on save"),
  #   ]),
}


def run_cl(argv=[]):
  logging.basicConfig(level=logging.INFO)
  
  try:
    app = MultioptParser(
      clsname='floyd',
      version=floyd.get_version(),
      desc_short="Static website generator",
      global_options=[
        make_option("-v", "--verbose", action="store_true", dest="verbose"),
        make_option("-d", "--debug", action="store_true", dest="debug"),
      ],
      command_set=commands,
      add_help=True,
      add_version=True)
    return app.run()
  except KeyboardInterrupt:
    cl_error('Interrupted.')
    return 1

def cl_error(msg=""):
  print >> sys.stderr, msg

