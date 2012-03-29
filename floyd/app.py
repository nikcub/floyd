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

import optparse



class CommandError(Exception): pass

class ArgumentError(Exception): pass

class OptionError(Exception): pass

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



class SubCommand(object):
  def __init__(self, func, usage, desc_short, options=None, arguments=[],desc_long='', common=True, header=None, footer=None):
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


class GlobalCommand(object):
  clsname = None
  version = 0
  _parser = None
  help_str = ""
  
  def __init__(self, header=None, footer=None, options=None):
    self.header = header
    self.footer = footer
    self.option_set = options
  
  def set_help(self, help_str):
    self.help_str = help_str

  def get_parser(self):
    self._parser= optparse.OptionParser(
      description='description',
      prog=self.clsname,
      version=self.version,
      epilog=self.footer,
      usage="%prog <command> [options] [arguments]\n\n" + self.help_str
    )
    self.option_set.parse_options(self._parser)
    return self._parser

class CommandOptions(object):
  parser = None
  parser_class = optparse.OptionParser
  option_key = ['short_name', 'long_name', 'type', 'default', 'help', 'dest']
  options = []

  def __init__(self, *args):
    for arg in args:
      if isinstance(arg, list):
        self.options.append(dict(zip(self.option_key, arg)))
      elif isinstance(arg, dict):
        self.options.append(arg)
      else:
        raise OptionError("Not a valid option: %s" % str(arg))


  def init_parser(self):
    self.parser = self.parser_class()

  def valid_option(self, option):
    if not set(option.keys()).issubset(set(self.option_key)):
      inv_option = list(set(option.keys()).difference(set(self.option_key)))[0]
      inv_option_val = option[inv_option]
      raise OptionError("Not a valid option argument: %s %s" % (inv_option, inv_option_val))
    return True

  def parse_options(self, parser):

    if not isinstance(parser, self.parser_class):
      raise Exception('invalid parser')

    for option in self.options:
      if self.valid_option(option):
        args = {
          'action': 'store',
        }
        if 'help' in option and option['help']:
          args['help'] = option['help']
        if option['type'] == bool:
          if option['default'] == True:
            args['action'] = 'store_false'
            args['default'] = True
          else:
            args['action'] = 'store_true'
            args['default'] = False
        parser.add_option(
            '-' + option['short_name'], 
            '--' + option['long_name'],
            **args
            # type=store_type
          )
        # print "added: %s %s %s " % (option['short_name'], option['long_name'], args)


class ClApp(object):
  """Singleton class to handle command line application
  
  Parses all command line options and commands and executes commands
  with passed options.
  """
  
  def __init__(self, argv, command_set, clsname='', version='', global_options=None):
    """docstring for __init__"""
    self.argv = argv
    self.clsname = clsname
    self.version = version
    self.command_set = command_set
    self.parser_class = optparse.OptionParser
    
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
    raise ArgumentError()

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

    if len(self.argv) < 2 or self.argv[1] not in self.command_set:
      self.parser.print_help()
      return 1
    
    basecommand = self.argv.pop(0)
    subcommand = self.argv.pop(1)
    
    print basecommand
    print subcommand
    print self.argv
    
    self.options, self.args = self.parser.parse_args(self.argv[1:])    
    
    print self.options
    print self.args
    
    command = self.args.pop(0)
    
    if command not in self.command_set:
      self.parser.error(self.print_help())
      
    print 'running %s' % command
    self.command_set[command].func()
    
    return 1
    curdir = os.getcwd()
    try:
      print args
    
      for arg in args:
        pass
    
      path_source = os.path.join(curdir, options.src)
      path_output = os.path.join(curdir, options.out)
      path_templates = os.path.join(curdir, 'templates')
      template_name = options.template
      path_template = os.path.join(path_templates, template_name)
    
      if not os.path.isdir(path_source):
        parser.error('Not a valid source directory: %s' % path_source)
      if not os.path.isdir(path_output):
        parser.error('Not a valid output directory: %s' % path_output)
      if not os.path.isdir(path_template):
        parser.error('Not a valid template directory or template: %s' % path_templates)

      floyd.templating.jinja.setup(path_template)
      floyd.db.setup(path_source)

      posts = floyd.db.Query('Posts').filter(post_type='post').filter(post_status='published').fetch(100)
      drafts = floyd.db.Query('Posts').filter(post_type='post').filter(post_status='draft').fetch(100)
      pages = floyd.db.Query('Posts').filter(post_type='page').fetch(100)
    except Exception, e:
      print "Error: %s" % str(e)
    
    return 1