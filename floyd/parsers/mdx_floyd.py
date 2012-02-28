#!/usr/bin/env python

"""Floyd markdown extension.

Implements:

 * New-line within paragraph inserts break (from Github flavored markdown)
"""

import re
import markdown

class FloydExtension(markdown.Extension):
  """Floyd markdown extension"""
  
  def __init__(self, configs):
    self.config = {}
  
  def extendMarkdown(self, md, md_globals):
    md.registerExtension(self)
    self.parser = md.parser
  
  def reset(self):
    pass

def makeExtension(configs=[]):
  return FloydExtension(configs=configs)