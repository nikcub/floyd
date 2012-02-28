#!/usr/bin/env python

"""Markdown time extension

implements `time` html5 attribute in markdown

"""

import re
import markdown

class TimeExtension(markdown.Extension):
  """Microdata extension"""
  
  def __init__(self, configs):
    self.config = {}
  
  def extendMarkdown(self, md, md_globals):
    md.registerExtension(self)
    self.parser = md.parser
  
  def reset(self):
    pass

def makeExtension(configs=[]):
  return TimeExtension(configs=configs)