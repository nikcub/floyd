#!/usr/bin/env python

"""Floyd markdown extension.

Implements:

 * New-line within paragraph inserts break (from Github flavored markdown)
 * numbered headings eg. h1. Heading
 * fenced code with ````
 
"""

import re
import markdown

# Global vars
FENCED_BLOCK_RE = re.compile(r'(?P<fence>^`{3,})[ ]*(?P<lang>[a-zA-Z0-9_-]*)[ ]*\n(?P<code>.*?)(?P=fence)[ ]*$', re.MULTILINE|re.DOTALL)
CODE_WRAP = '<p><pre%s>%s</pre></p>'
LANG_TAG = ' class="%s"'

def newline_callback(matchobj):
  if len(matchobj.group(1)) == 1:
    return matchobj.group(0).rstrip() + '  \n'
  else:
    return matchobj.group(0)

class FloydExtension(markdown.Extension):
  """Floyd markdown extension"""
  
  def __init__(self, configs):
    self.config = {}
  
  def extendMarkdown(self, md, md_globals):
    md.registerExtension(self)
    md.parser.blockprocessors.add('dotheader', DotHeaderProcessor(md.parser), '_begin')
    md.preprocessors.add('fenced_code_block', FencedBlockPreprocessor(md), "_begin")
    md.preprocessors.add('double_nl', DoubleNewlinePreprocessor(md), "_begin")
    #self.processor = DotHeaderProcessor(md.parser)
    #self.processor.md = md
    #self.parser = md.parser
  
  def reset(self):
    pass

class FencedBlockPreprocessor(markdown.preprocessors.Preprocessor):
  def run(self, lines):
    text = '\n'.join(lines)
    m = FENCED_BLOCK_RE.search(text)
    if m:
      lang = ''
      if m.group('lang'):
          lang = LANG_TAG % m.group('lang')
      code = CODE_WRAP % (lang, self._escape(m.group('code')))
      placeholder = self.markdown.htmlStash.store(code, safe=True)
      text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
    return text.split('\n')
  
  def _escape(self, txt):
    return txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
  
class DoubleNewlinePreprocessor(markdown.preprocessors.Preprocessor):
  def run(self, lines):
    text = '\n'.join(lines)
    text = re.sub(r'^[\w\<][^\n]*(\n+)', newline_callback, text)
    return text.split('\n')

class DotHeaderProcessor(markdown.blockprocessors.HashHeaderProcessor):
  """Process numbered headers"""
  RE = re.compile(r'(^|\n)(?P<level>h[1-6]\.)(?P<header>.*?)#*(\n|$)')

  def test(self, parent, block):
    return bool(self.RE.search(block))

  def run(self, parent, blocks):
    block = blocks.pop(0)
    m = self.RE.search(block)
    if m:
      before = block[:m.start()] # All lines before header
      after = block[m.end():]    # All lines after header
      if before:
        self.parser.parseBlocks(parent, [before])
      # Create header using named groups from RE
      h = markdown.etree.SubElement(parent, m.group('level')[:2])
      h.text = m.group('header').strip()
      if after:
        blocks.insert(0, after)
    else:
      message(CRITICAL, "We've got a problem header!")

def makeExtension(configs=[]):
  return FloydExtension(configs=configs)