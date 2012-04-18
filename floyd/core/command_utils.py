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
"""

import os
import sys
import logging

import floyd.core.commands
from floyd.core.multiopt import SubCommand, GlobalCommand, make_option



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
  '_global': GlobalCommand(
    header="help header",
    options=[
      make_option("-v", "--verbose", action="store_true", dest="verbose"),
      make_option("-d", "--debug", action="store_true", dest="debug"),
      make_option("-z", "--zoo", action="store_true", dest="zoo", help="zoo fuck"),
    ]
  ),
  
  'help': SubCommand(
    func=floyd.core.commands.help,
    usage='%prog help [command]',
    desc_short='print help for a command',
    arguments=['command'],
    options=[]
  ),

  'init': SubCommand(
    func=floyd.core.commands.help,
    usage='%prog init [options] <directory>',
    desc_short='Initialize a new site directory',
    desc_long="""
Generates a new site with a template in directory
specified by <directory> or by default in the
current directory""",
    options=[
    ]
  ),

  'generate': SubCommand(
    func=floyd.core.commands.generate,
    usage='%prog help [command]',
    desc_short='Generate a new site',
    options=[
      make_option('-t', '--template', action="store", type="string", dest="filename"),
      make_option('-z', '--zoo', action="store", type="string", dest="zoo")
    ]),

  'deploy': SubCommand(
    func=floyd.core.commands.help,
    usage='%prog help [command]',
    desc_short='Deploy a site'),

  'serve': SubCommand(
    func=floyd.core.commands.help,
    usage='%prog help [command]',
    desc_short='Run local server instance'),

  'watch': SubCommand(
    func=floyd.core.commands.help,
    usage='%prog help [command]',
    desc_short='Watch site and auto-deploy on save'),
}


def run_cl(argv=[]):
  logging.basicConfig(level=logging.INFO)
  
  try:
    app = floyd.core.multiopt.Multiopt(
      clsname='floyd',
      version=floyd.get_version(),
      command_set=commands)
    return app.run()
  except KeyboardInterrupt:
    cl_error('Interrupted.')
    return 1

def cl_error(msg=""):
  print >> sys.stderr, msg

