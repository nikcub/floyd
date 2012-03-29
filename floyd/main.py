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
import time
import yaml

import floyd

import floyd.app


import floyd.commands
# import floyd.util.const as const
# import floyd.app.Command as Command
from floyd.app import SubCommand, CommandOptions, GlobalCommand

TIMER_START = time.time()

VERBOSITY = 2

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

_DEFAULT_GENERATOR = [
  # (post.stub in floyd.db.Query('Posts').filter(post_type='post').filter(post_status='published').fetch(100))
  # map(post, posts)
  # or list expression
  # [controllers.post(p, '/posts/<stub>') for p in posts]
]
# @TODO this can be a lot better
_TITLE_MATCH = re.compile('<h1 id="title">(.*)</h1>')


commands = {
  '_global': GlobalCommand(
    header="help header",
    options=CommandOptions(
      ["v", "verbose", bool, False], 
      ["d", "debug", bool, False, "show debugz information"]
    )
  ),
  
  'help': SubCommand(
    func=floyd.commands.help,
    usage='%prog help [command]',
    desc_short='print help for a command',
    arguments=['command'],
    options=CommandOptions(
      
    )),

  'init': SubCommand(
    func=floyd.commands.help,
    usage='%prog init [options] <directory>',
    desc_short='Initialize a new site directory',
    desc_long="""
Generates a new site with a template in directory
specified by <directory> or by default in the
current directory""",
    options=CommandOptions(
      ["t", "template", str, None, "use template directory"]
    )),

  'generate': SubCommand(
    func=floyd.commands.help,
    usage='%prog help [command]',
    desc_short='Generate a new site'),

  'deploy': SubCommand(
    func=floyd.commands.help,
    usage='%prog help [command]',
    desc_short='Deploy a site'),

  'serve': SubCommand(
    func=floyd.commands.help,
    usage='%prog help [command]',
    desc_short='Run local server instance'),

  'watch': SubCommand(
    func=floyd.commands.help,
    usage='%prog help [command]',
    desc_short='Watch site and auto-deploy on save'),
}


def Main(argv):
  logging.basicConfig(level=logging.INFO)
  
  try:
    app = floyd.app.ClApp(
      argv=argv,
      clsname=floyd.__clsname__,
      version=floyd.__version__,
      command_set=commands)
    sys.exit(app.run())
  except KeyboardInterrupt:
    cl_error('Interrupted.')
    sys.exit(1)

def cl_error(msg=""):
  if VERBOSITY > 1:
    print >>sys.stderr, msg
    
if __name__ == '__main__':
  Main(sys.argv)
