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
""" Floyd - server

serves floyd sites on a local http server
"""


import os
import sys
import threading
import re
import logging
import posixpath

from urlparse import urlparse
from urllib import unquote
from floyd import get_version

import BaseHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from SocketServer import ThreadingMixIn
from SimpleHTTPServer import SimpleHTTPRequestHandler

__version__ = get_version()
server_config = {}

class ServerException(Exception): pass

class Server(object):
  def __init__(self, path, port='8080', address='127.0.0.1'):
    if not os.path.isdir(path):
      raise ServerException('Not a valid directory to serve from: %s' % path)
    server_config['path'] = path
    self.path = path
    self.port = int(port)
    self.address = address
    self.running = False
    self.httpd = HTTPServer((address, port), StaticRequestHandler)
    self.sock = self.httpd.socket.getsockname()
  
  def run(self):
    logging.info("Serving on %s:%d from %s" % (self.sock[0], self.sock[1], self.path))
    self.running = True
    self.httpd.serve_forever()
  
  def stop(self):
    logging.info("Stopping server")
    self.httpd.shutdown()
    self.httpd.socket.close()
    
class HTTPServer(BaseHTTPServer.HTTPServer):
  def __init__(self, *args, **kwargs):
    BaseHTTPServer.HTTPServer.__init__(self, *args, **kwargs)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer): 
  """Threaded HTTP Server
  """

class DynamicRequestHandler(CGIHTTPRequestHandler): pass
  """ @TODO implement CGI exec for admin
  
   * route map support etc.
  """

class StaticRequestHandler(SimpleHTTPRequestHandler):
  """Default floyd request handler for static
  """
  protocol_version = "HTTP/1.0"
  sys_version = ''
  server_version = "floyd/%s" % __version__
  default_files = ['index', 'index.html']
  default_content_type = "text/html"
  default_charset = "utf-8"
  content_header = "%s; charset=%s"

  def __init__(self, *args, **kwargs):
    if 'path' in server_config:
      self.base_path = server_config['path']
    else:
      self.base_path = 'site'
    SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

  def log_message(self, format, *args):
    logging.info("%s - %s" % (self.log_date_time_string(), format % args))

  def guess_type(self, path):
    self.extensions_map.update({
    '': self.default_content_type
    })
    base, ext = posixpath.splitext(path)
    if ext in self.extensions_map:
      return self.extensions_map[ext]
    ext = ext.lower()
    if ext in self.extensions_map:
      return self.extensions_map[ext]
    else:
      return self.extensions_map['']

  def translate_path(self, path):
    fpath = self.base_path
    path = unquote(path.split('#',1)[0].split('?',1)[0])
    parts = filter(None, path.split('/'))
    for part in parts:
      if part in (os.curdir, os.pardir): continue
      fpath = os.path.join(fpath, part)
    if os.path.isdir(fpath):
      for i in self.default_files:
        dir_index = os.path.join(fpath, i)
        if os.path.isfile(dir_index):
          return dir_index
    return fpath
