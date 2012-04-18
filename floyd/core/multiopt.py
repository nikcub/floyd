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
"""Floyd main application class
"""

import sys
import optparse
from optparse import make_option


class CommandError(Exception): pass

class ArgumentError(Exception): pass

class OptionError(Exception): pass

class LaxOptionParser(optparse.OptionParser):
  """
  An option parser that doesn't raise any errors on unknown options.
  """
  def error(self, msg):
    pass

  def print_help(self):
    """Output nothing.

    The lax options are included in the normal option parser, so under
    normal usage, we don't need to print the lax options.
    """
    pass

  def print_lax_help(self):
    """Output the basic options available to every command.

    This just redirects to the default print_help() behavior.
    """
    optparse.OptionParser.print_help(self)

  def _process_args(self, largs, rargs, values):
    """
    Overrides OptionParser._process_args to exclusively handle default
    options and ignore args and other options.

    This overrides the behavior of the super class, which stop parsing
    at the first unrecognized option.
    """
    while rargs:
      arg = rargs[0]
      try:
        if arg[0:2] == "--" and len(arg) > 2:
          # process a single long option (possibly with value(s))
          # the superclass code pops the arg off rargs
          self._process_long_opt(rargs, values)
        elif arg[:1] == "-" and len(arg) > 1:
          # process a cluster of short options (possibly with
          # value(s) for the last one only)
          # the superclass code pops the arg off rargs
          self._process_short_opts(rargs, values)
        else:
          # it's either a non-default option or an arg
          # either way, add it to the args list so we can keep
          # dealing with options
          del rargs[0]
          raise Exception
      except:
        largs.append(arg)

# parser = OptionParser(usage="%prog [options]", prog=floyd.__clsname__, version="floyd v%s" % (floyd.__version__))
# parser = argparse.ArgumentParser(description='Static website generator for cloud hosting platforms', epilog='Report any issues to [Github url]')
# parser.add_option('-s','--src', dest='src', type='string', default='sources', help='Project source ("src" by default)')
# parser.add_option('-d','--dir', dest='out', type='string', default='site', help='The directory in which to create site (creates in "site" by default)')
# parser.add_option('-t','--template', dest='template', type='string', default='default', help='Template to use (\'default\' by default)')
# parser.add_option('-p', dest='pyfile', type='string', default='', help='read config from python file')
# @TODO watcher
# parser.add_option('-w','--watch', dest='out', type='string', default='site', help='Watch contents and automatically render and deploy')
# @TODO local server
# parser.add_option('-s', '--server', dest='server', action='store_true', default=False, help='server')


class BaseCommand(object):
  """
  """
  option_set = []
  
  def __init__(self, header=None, footer=None, options=None):
    self.header = header
    self.footer = footer
    if type(options) == type([]):
      self.option_set = options

  def set_help(self, help_str):
    self.help_str = help_str

  def get_parser(self):
    self._parser= LaxOptionParser(
      description='description',
      prog=self.clsname,
      version=self.version,
      epilog=self.footer,
      usage="%prog <command> [options] [arguments]\n\n" + self.help_str
    )
    for option in self.option_set:
      if isinstance(option, optparse.Option):
        self._parser.add_option(option)
      else:
        raise OptionError('invalid option')
    return self._parser

class SubCommand(BaseCommand):
  def __init__(self, func, usage, desc_short, options=None, arguments=[], desc_long='', common=True, header=None, footer=None):
    self.func = func
    self.usage = usage
    self.desc_short = desc_short
    self.optionset = options
    self.arguments = arguments
    self.desc_long = desc_long
    self.common = common
    self.header = header
    self.footer = footer
    
    self.parser_class = optparse.OptionParser
  
  def init_optionset():
    pass

  def __call__(self, func):
    meth = getattr(self, func)
    print 'calling: %s ' % func
    return meth()


class GlobalCommand(BaseCommand):
  clsname = None
  version = 0
  _parser = None
  help_str = ""

  


class Multiopt(object):
  """class to handle command line application
  
  Parses all command line options and commands and executes commands
  with passed options.
  """
  
  def __init__(self, command_set, argv='', clsname='', version='', global_options=None):
    """docstring for __init__"""
    self.command_set = command_set
    self.argv = argv or sys.argv[1:]
    self.clsname = clsname or self.argv[0]
    self.version = version
    self.parser_class = LaxOptionParser
    
    if '_global' in self.command_set:
      self.global_options = self.command_set.pop('_global')
    else:
      self.global_options = GlobalCommand()
    
    self.global_options.clsname = clsname
    self.global_options.version = version
    

  def print_help(self):
    """docstring for fname"""    
    # self.parser.print_help()
    help = 'Command must be one of:\n%s' % self.get_commands()
    help += 'See \'%s help COMMAND\' for help and information on a command' % self.clsname
    return help

  def get_commands(self):
    description = ""
    action_names = self.command_set.keys()
    action_names.sort()
    for action_name in action_names:
      description += "   %-10s %-70s\n" % (action_name, self.command_set[action_name].desc_short.capitalize())
    return description

  def run(self):
    self.global_options.set_help(self.print_help())
    self.parser = self.global_options.get_parser()
    
    self.options, self.args = self.parser.parse_args(self.argv)    
    
    if len(self.args) < 1:
      self.parser.print_lax_help()
      return 2
    
    if self.args[0] not in self.command_set:
      self.parser.print_lax_help()
      return 2
      
    try:
      command = self.args.pop(0)
      self.command_set[command].func(self.options, *self.args)
    except CommandError, e:
      print "Command Error: %s\n" % str(e)
      # @TODO show command help
      # self.parser.print_lax_help()
      return 2

      
    return 1
