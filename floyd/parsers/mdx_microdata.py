#!/usr/bin/env python

"""Markdown microdata extension

This will eventually implement microdata and common schema's within markdown
"""

import re
import markdown

class MicrodataExtension(markdown.Extension):
  """Microdata extension"""
  
  def __init__(self, configs):
    self.config = {}
  
  def extendMarkdown(self, md, md_globals):
    md.registerExtension(self)
    self.parser = md.parser
  
  def reset(self):
    pass

def makeExtension(configs=[]):
  return MicrodataExtension(configs=configs)